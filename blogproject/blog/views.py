from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from blog.models import Post
from django.views.generic import ListView
from blog.forms import CommentsForm
# Create your views here.

#Class Baased View implementing pagination
class PostListView(ListView):
    model=Post
    #sets the post count per page
    paginate_by = 2

from taggit.models import Tag
#View displaying List of posts
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    #Pagination concept
    paginator=Paginator(post_list,2)
    #Here creating a paginator that displays 3 posts per page
    page_number = request.GET.get("page")
    #Related to the page number get the list
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:    #If page number is not sent=> by default display first page
        post_list=paginator.page(1)
    except EmptyPage:   #if there is no next page
        post_list=paginator.page(paginator.num_pages)
    my_dict = {'post_list':post_list,'tag':tag}
    return render(request, 'blog/post_list.html', my_dict)


#View displaying details of a post
#Also displays the comments section
def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status="published",
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    comments = post.comments.filter(active=True)
    csubmit=False # when comment is not submitted
    if request.method=="POST":
        form=CommentsForm(request.POST)
        if form.is_valid():
            #save the form , but do not commit
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentsForm()

    return render(request, "blog/post_detail.html",{'post':post,'form':form,'csubmit':csubmit,'comments':comments})


from django.core.mail import send_mail
from blog.forms import EmailSendForm

def mail_send_view(request,id):
    #id : unique identifier of Post
    post = get_object_or_404(Post, id=id,status="published")
    sent=False
    if request.method=="POST":
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            #read data and send memail
            #send_mail('subject','message','sender',['receiver'])
            subject = '{}({}) recommends you to  read {}'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message = 'Read Post At:\n {}\n\n{}\'s Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            print("subject :",subject)
            print("message :",message)
            #commented out below line as emails not being sent successfully using gmail SMTP server
            #send_mail(subject,message,sender,[cd['to']])
            sent=True
    else:
        form = EmailSendForm()
    return render(request,"blog/sharebymail.html",{'form':form,'post':post,'sent':sent})
