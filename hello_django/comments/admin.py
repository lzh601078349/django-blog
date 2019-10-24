from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk', 'email', 'url', 'post', 'created_time']
    fields = ['name', 'email', 'url', 'text', 'post']
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 5


admin.site.register(Comment, CommentAdmin)
# Register your models here.
