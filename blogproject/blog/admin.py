from django.contrib import admin
from blog.models import Post,Comments
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','body','publish','created','updated','status']
    #populate fields based on some other field
    #This is a dictionary
    prepopulated_fields={'slug':('title',)}
    #To filter records based on some info
    #below filter based on status or author or created or publish
    list_filter=('status','author',"created","publish")
    #search option: to search by specified fields
    search_fields=('title','body')
    #to choose data based on the author id
    raw_id_fields=('author',)
    #date hierarchy,displayed at top of the posts
    date_hierarchy="publish"
    ordering=['status','publish']

class CommentsAdmin(admin.ModelAdmin):
    list_display=["name","email","post","body","created","updated","active"]
    list_filter=("active",'created',"updated")
    search_fields=("name","email","body")


admin.site.register(Post,PostAdmin)
admin.site.register(Comments,CommentsAdmin)
