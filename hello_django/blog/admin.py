from django.contrib import admin
from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "pk", "created_time",
                    "modified_time", "category", "author"]
    fields = ["title", "body", "category", "tags"]
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

# Register your models here.
