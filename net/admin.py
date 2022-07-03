from django.contrib import admin
from .models import User, Post, Comment, Profile
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('follower',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'post')
    filter_horizontal = ('likes', )

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)