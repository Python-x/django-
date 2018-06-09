from django.shortcuts import render
from .models import Banner, Post, Comment, FriendlyLink, BlogCategory, Tags
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
from django.views.generic.base import View
from django.db.models import Q


def detail(request, pid):
    vieww = Post.objects.get(id=pid)
    vieww.views+=1
    vieww.save()
    tags_list = vieww.tags
    about_recomment = []
    for tag in tags_list.all():
        about_recomment.extend(tag.post_set.all())
    comment_list = Comment.objects.order_by('-pub_date')
    comment_list2 = []
    for piw in comment_list:
        if piw.post not in comment_list2:
            comment_list2.append(piw.post)
    cds = {
        'views':vieww,
        'about_recomment':about_recomment,
        'comment_list': comment_list2,
    }
    return render(request,'show.html', cds)



class Search(View):
    def get(self, request):
        pass

    def post(self, request):
        keywords = request.POST.get('keyword')
        postlist = Post.objects.filter(Q(title__contains=keywords) | Q(content__contains=keywords))
        tags = Tags.objects.all()
        comment_list = Comment.objects.order_by('-pub_date')
        comment_list2 = []
        for piw in comment_list:
            if piw.post not in comment_list2:
                comment_list2.append(piw.post)
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1

        # objects = ['john', 'edward', 'josh', 'frank']
        p = Paginator(postlist, per_page=2, request=request)

        people = p.page(page)
        cdx = {
            'postlist': postlist,
            'people':people,
            'tags_list': tags,
            'comment_list': comment_list2,
        }
        return render(request, 'list.html', cdx)


# Create your views here.
def index(request):
    #所有post
    banner_list = Banner.objects.all()
    #倒序post
    banner_filter3 = Post.objects.order_by('-pub_date')
    #推荐
    banner_filter = Post.objects.filter(is_recomment=True)
    #评论
    comment_list = Comment.objects.order_by('-pub_date')
    comment_list2 = []

    try:
        page = request.GET.get('page', 1)
    except:
        page = 1

    # objects = ['john', 'edward', 'josh', 'frank']
    p = Paginator(banner_filter3, per_page=2, request=request)

    people = p.page(page)
    for i in banner_filter3:
        i.content = i.content[:20]
    for i2 in banner_filter:
        i2.content = i2.content[:20]
    for piw in comment_list:
        if piw.post not in comment_list2:
            comment_list2.append(piw.post)
    friendlylink_list = FriendlyLink.objects.all()
    blogcategory_list = BlogCategory.objects.all()
    ctx = {
        'people':people,
        'banner_list': banner_list,
        'banner_filter2': banner_filter,
        'banner_filter3': banner_filter3,
        'comment_list': comment_list2,
        'friendlylink_list': friendlylink_list,
        'blogcategory_list': blogcategory_list,
    }
    return render(request, 'index.html', ctx)


def list1(request, tid=-1, cid = -1):
    if tid != -1:
        Post1 = Post.objects.filter(tags=tid)
    elif cid != -1:
        Post1 = Post.objects.filter(category=cid)
    else:
        Post1 = Post.objects.order_by('-pub_date')
    comment_list = Comment.objects.order_by('-pub_date')
    comment_list2 = []
    tags = Tags.objects.all()
    for po in Post1:
        po.content = po.content[:20]
    for piw in comment_list:
        if piw.post not in comment_list2:
            comment_list2.append(piw.post)
    try:
        page = request.GET.get('page', 1)
    except:
        page = 1

    # objects = ['john', 'edward', 'josh', 'frank']
    p = Paginator(Post1, per_page=2, request=request)

    people = p.page(page)
    cdd = {
        'postlist': Post1,
        'comment_list': comment_list2,
        'people': people,
        'tags_list': tags,
    }
    return render(request, 'list.html', cdd)
