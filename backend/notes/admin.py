from django.contrib import admin
from .models import Note, NoteBookmark, NoteProgress, NoteRevision

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title','subject','grade','status','created_by','updated_at')
    list_filter = ('status','subject','grade')
    search_fields = ('title','subtitle','subject','created_by__username')
    readonly_fields = ('created_at','updated_at','published_at','view_count')

admin.site.register(NoteBookmark)
admin.site.register(NoteProgress)
admin.site.register(NoteRevision)
