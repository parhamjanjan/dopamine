from django.db import transaction
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Note, NoteBookmark, NoteProgress, NoteRevision
from .permissions import NotePermission, is_site_admin
from .serializers import NoteSerializer, ProgressSerializer, RevisionSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [NotePermission]
    lookup_field = 'id'

    def get_queryset(self):
        qs = Note.objects.select_related('created_by')
        if is_site_admin(self.request.user):
            return qs.all()
        return qs.filter(status=Note.PUBLISHED)

    def perform_create(self, serializer):
        if not is_site_admin(self.request.user):
            raise PermissionDenied('فقط مدیر سایت می‌تواند جزوه ایجاد کند.')
        note = serializer.save(created_by=self.request.user)
        if note.status == Note.PUBLISHED:
            note.published_at = timezone.now()
            note.save(update_fields=['published_at'])

    def perform_update(self, serializer):
        if not is_site_admin(self.request.user):
            raise PermissionDenied('فقط مدیر سایت می‌تواند جزوه را ویرایش کند.')
        old = self.get_object()
        snapshot = {key: getattr(old, key) for key in ['title','subtitle','subject','grade','cover_color','cover_icon','estimated_minutes','tags','chapters','blocks','status']}
        with transaction.atomic():
            NoteRevision.objects.create(note=old, editor=self.request.user, snapshot=snapshot)
            note = serializer.save()
            if note.status == Note.PUBLISHED and not note.published_at:
                note.published_at = timezone.now()
                note.save(update_fields=['published_at'])
            elif note.status == Note.DRAFT:
                note.published_at = None
                note.save(update_fields=['published_at'])

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        note = self.get_object()
        if note.status == Note.PUBLISHED:
            Note.objects.filter(pk=note.pk).update(view_count=note.view_count + 1)
        return response

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def bookmark(self, request, id=None):
        note = self.get_object()
        if note.status != Note.PUBLISHED and not is_site_admin(request.user):
            raise PermissionDenied('این جزوه منتشر نشده است.')
        item, created = NoteBookmark.objects.get_or_create(user=request.user, note=note)
        if not created:
            item.delete()
        return Response({'bookmarked': created})

    @action(detail=True, methods=['get','put'], permission_classes=[permissions.IsAuthenticated])
    def progress(self, request, id=None):
        note = self.get_object()
        if note.status != Note.PUBLISHED and not is_site_admin(request.user):
            raise PermissionDenied('این جزوه منتشر نشده است.')
        progress, _ = NoteProgress.objects.get_or_create(user=request.user, note=note)
        if request.method == 'GET':
            return Response(ProgressSerializer(progress).data)
        serializer = ProgressSerializer(progress, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        if not is_site_admin(request.user):
            raise PermissionDenied('فقط مدیر سایت به جزوه‌های پیش‌نویس دسترسی دارد.')
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def bookmarks(self, request):
        ids = NoteBookmark.objects.filter(user=request.user).values_list('note_id', flat=True)
        notes = Note.objects.filter(id__in=ids, status=Note.PUBLISHED).select_related('created_by')
        return Response(self.get_serializer(notes, many=True).data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def revisions(self, request, id=None):
        if not is_site_admin(request.user):
            raise PermissionDenied('فقط مدیر سایت به تاریخچه دسترسی دارد.')
        note = self.get_object()
        return Response(RevisionSerializer(note.revisions.select_related('editor'), many=True).data)
