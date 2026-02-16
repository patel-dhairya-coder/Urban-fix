from django.contrib import admin
from django.utils.html import format_html
from .models import Complaint

class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'report_id', 'user', 'category', 'location',
        'status', 'submitted_at', 'image_tag')

    def image_tag(self, obj):
        if not obj.photo:
            return "No Image"
        
        try:
            # Check if file exists on disk
            if obj.photo.name and obj.photo.storage.exists(obj.photo.name):
                return format_html(
                    '<img src="{}" width="100" height="auto" '
                    'style="max-height: 100px; object-fit: cover; border-radius: 4px;" '
                    'onerror="this.style.display=\'none\'; this.nextSibling.style.display=\'inline\';" />'
                    '<span style="display:none; color: #999; font-size: 12px;">Image Error</span>',
                    obj.photo.url
                )
            else:
                return '<span style="color: #999;">File Missing</span>'
        except (ValueError, IOError, OSError) as e:
            return f'<span style="color: #red;">Error: {str(e)[:20]}...</span>'
    
    image_tag.short_description = 'Photo'
    image_tag.allow_tags = True
    
list_filter = ('status', 'category', 'submitted_at')
search_fields = ('description', 'location', 'user__username')
date_hierarchy = 'submitted_at'
readonly_fields = ['submitted_at']

fieldsets = (
        (None, {
            'fields': (
                'user', 'category', 'location', 'description',
                'photo'
            )
        }),
        ('Status Information', {
            'fields': ('status', 'submitted_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Complaint,ComplaintAdmin)