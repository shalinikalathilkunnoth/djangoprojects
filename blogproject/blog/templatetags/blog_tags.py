from blog.models import Post
from django import template
register=template.Library()

#Creating custom template tags
@register.simple_tag(name='postcount')
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('blog/latest_posts123.html')
def show_latest_posts(count=3):
    latest_posts=Post.objects.order_by("-publish")[0:count]
    return {'latest_posts':latest_posts}

from django.db.models import Count
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]