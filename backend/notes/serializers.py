import re
from rest_framework import serializers
from .models import Note, NoteProgress, NoteRevision

class NoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id','title','subtitle','subject','grade','cover_color','cover_icon','estimated_minutes','tags','chapters','blocks','status','created_by','created_by_name','created_at','updated_at','published_at','view_count','is_bookmarked','progress_percent']
        read_only_fields = ['id','created_by','created_at','updated_at','published_at','view_count','created_by_name','is_bookmarked','progress_percent']

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() or obj.created_by.username

    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        return bool(user.is_authenticated and obj.bookmarks.filter(user=user).exists())

    def get_progress_percent(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        progress = obj.progress_records.filter(user=user).only('percent').first()
        return progress.percent if progress else 0

    def validate_cover_color(self, value):
        if not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
            raise serializers.ValidationError('رنگ باید به شکل #7055e8 باشد.')
        return value

    def validate_blocks(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('محتوای جزوه باید فهرستی از بلوک‌ها باشد.')
        if len(value) > 500:
            raise serializers.ValidationError('تعداد بلوک‌ها بیش از حد مجاز است.')
        for i, block in enumerate(value):
            if not isinstance(block, dict) or not isinstance(block.get('type'), str):
                raise serializers.ValidationError(f'ساختار بلوک شماره {i + 1} معتبر نیست.')
        return value

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteProgress
        fields = ['completed_blocks','last_block','percent','updated_at']
        read_only_fields = ['updated_at']
    def validate_percent(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError('درصد باید بین صفر تا صد باشد.')
        return value

class RevisionSerializer(serializers.ModelSerializer):
    editor_name = serializers.SerializerMethodField()
    class Meta:
        model = NoteRevision
        fields = ['id','editor_name','snapshot','created_at']
    def get_editor_name(self, obj):
        return obj.editor.get_full_name() or obj.editor.username
