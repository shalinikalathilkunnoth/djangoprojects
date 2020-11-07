from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class CustomManager(models.Manager):
    #Filtering to show only published posts
    def get_queryset(self):
        return super().get_queryset().filter(status="published")

from taggit.managers import TaggableManager
class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=264,unique_for_date='publish')
    author = models.ForeignKey(User, related_name="blog_posts",  on_delete=models.CASCADE)
    body = models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True) #current time when post created will be considered
    updated=models.DateTimeField(auto_now=True) #When save() method is called on the model
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    #custom manager that returns only published posts
    objects=CustomManager()
    #Tag Manager to manage all the tags related to post
    tags = TaggableManager()

    class Meta:
        ordering=('-publish',)    #default reverse natural sorting : Desc order of publish field

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])

#model related to comments section
#comments associated with Post
#A post can have multiple comments hence one - to - many relation
class Comments(models.Model):
    #related_name="comments",used to get post related comments
    post=models.ForeignKey(Post,related_name="comments",  on_delete=models.CASCADE)
    name=models.CharField(max_length=32)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=('-created',)

    def __str__(self):
        return "Commented By {} on {}".format(self.name,self.post)
