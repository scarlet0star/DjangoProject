from django.contrib import admin
from .models import *
# Register your models here.

#admin.site.register(Board)
#admin.site.register(Post)
#admin.site.register(Comment)

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('pk','subject','principal','isActivate')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk','title','PostAuthor','writeDate')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('CommentAuthor','contents','writeDate')