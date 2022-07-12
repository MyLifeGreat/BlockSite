from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.
# # email sending
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag





def post_list(request,tag_slug=None):
    object_list = Post.objects.filter(status="published")
    # hashtag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list,2)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        "posts":posts,
        "page":page,
        "tag":tag,
    }    
    return render(request,'blog/post/list.html',context)


def post_detail(request,year,month,day,post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year = year,
        publish__month = month,
        publish__day  = day
    )
    # # Comments
    comments = post.comments.filter(active=True) # #
    new_comment = None
    if request.method == 'POST': # # 
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        "post":post,
        "comments":comments,
        "new_comment":new_comment,
        "comment_form":comment_form, 
    }
    return render(request, 'blog/post/detail.html',context)

# # Email send
def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST) # # formani ichida post qilinyatgon narsani ovoladi
        if form.is_valid(): # # formani togriligini tekshiradi
            cd = form.cleaned_data # # formadan xosil bolgan obektlarni dikshiniri korinishda ovoladi
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} sizga {post.title} ni o'qishni tavsiya qiladi."
            message = f"Salom, yaxshimisiz?. Quyidagi linkdagi postni o'qib ko'ring.{post_url}\n\nComents:{cd['comments']}"
            send_mail(subject,message,settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post':post,'form':form,'sent':sent})
