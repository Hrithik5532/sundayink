
from datetime import date
from logging import raiseExceptions
from re import I
from django.contrib import messages
from .forms import PostForm, SubscribeForm,ContactForm
from django.shortcuts import render , get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Post, Category,BlogComment, ReplayComment, IpModel,SubcribeUsers,Contact
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q  # New

# -------------- Blog-single page----------------------------------------
# -----------------------------------------------------------
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def get_prev_next(id):
    b = get_object_or_404(Post, post_id=id)

    posts = Post.objects.alias().filter(post_now=True)

    for i in range(len(posts)):
        try:
            if b==posts[0]:
                next = posts[i+1]
                prev=None
                break
            elif b==posts.reverse()[0]:
                prev=posts.reverse()[i+1]
                next=None
                break
            else:
                if b==posts[i]:
                    next = posts[i+1]
                    prev = posts[i-1]
                    break
        except :
            prev=None
            next=None
    return prev, next

def homepage(request):
    try:
                ip = get_client_ip(request)
                if not IpModel.objects.filter(ip=ip).exists():
                    IpModel.objects.create(ip=ip)
                b=Post.objects.filter().filter(post_now=True).order_by('-post_date')

                if b[0].post_date <= date.today():
                        b=b[0]
                else:
                    b=b[1]
                comments = BlogComment.objects.filter(post=b)
                #replaycomments = ReplayComment.objects.filter(post=b).filter(parrent=comments)
                no_likes=b.like_post.count()
                liked = False
                #replaydic = {}
                ip_count = IpModel.objects.all().count()

                if b.like_post.filter(id=IpModel.objects.get(ip=ip).id).exists():
                    liked=True
                prev, next = get_prev_next(b.post_id)

                context = {
                        'b':b,
                        'no_likes':no_likes,
                        'liked':liked,
                        'comments':comments,
                        'ip_count':ip_count,
                          'next':next,
                'prev':prev
                     #   'replaycomments':replaycomments
                    }

                return  render(request,'blog-single.html',context)
                #return  render(request,'blog-single.html',context)


    except Exception as e:
        print(e)
        if IndexError:
            messages.info(request,'No Blog Posted')
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request,'404.html')


def home(request,pk):
     try:
        ip_count = IpModel.objects.all().count()

        b = get_object_or_404(Post, post_id=pk)
        ip = get_client_ip(request)


        if not IpModel.objects.filter(ip=ip).exists():
            IpModel.objects.create(ip=ip)
        if b.post_date <=date.today():
            if b.post_now ==True:
                prev, next = get_prev_next(pk)

                comments = BlogComment.objects.filter(post=b)

                no_likes=b.like_post.count
                liked = False
            #  print(b.like_post.filter(id=IpModel.objects.get(ip=ip).id))
                if b.like_post.filter(id=IpModel.objects.get(ip=ip).id).exists():
                        liked=True
                context = {
                    'b':b,
                    'no_likes':no_likes,
                    'liked':liked,
                    'comments':comments,
                    'ip_count':ip_count,
                    'next':next,
                    'prev':prev
                }
                return render(request,'blog-single.html',context)
        messages.info(request,'No Blog Posted')

        return HttpResponseRedirect(reverse('home'))

     except Exception as e:
        print(e)

        return render(request,'404.html')



def previewBlogsView(request,pk):
    try:
        ip = get_client_ip(request)
        if not IpModel.objects.filter(ip=ip).exists():
            IpModel.objects.create(ip=ip)
        b = get_object_or_404(Post, post_id=pk)
        comments = BlogComment.objects.filter(post=b)
        no_likes=b.like_post.count
        liked = False
        prev, next = None,None
        preview=True
        if b.like_post.filter(id=IpModel.objects.get(ip=ip).id).exists():
            liked=True


        ip_count = IpModel.objects.all().count()

        context = {
            'b':b,
            'no_likes':no_likes,
            'liked':liked,
            'comments':comments,
            'ip_count':ip_count,
            'next':next,
                'prev':prev,
                'preview':preview
        }

        return render(request,'blog-single.html',context)
    except Exception as e:
        print(e)
        return render(request,'404.html')






# --------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------

def BlogsView(request):
        try:
            categoryName = request.GET.get('categoryName')
            year = request.GET.get('year')

            if categoryName!='Select Category' or year!="Select Year":

                if year!="Select Year":
                    if categoryName !='Select Category':
                        cat = get_object_or_404(Category,cat_title=categoryName)
                        allposts= Post.objects.filter(category=cat.cat_id).filter(post_now=True)
                        post=[]
                        for p in allposts:
                            if p.post_date <= date.today():
                                posts.append(p)


                    else:
                        posts =Post.objects.filter(post_now=True)
                    post=[]
                    for p in posts :
                        if p.post_date <= date.today():
                            if p.post_date.year==int(year):
                                post.append(p)
                elif categoryName!='Select Category':

                    if year !="Select Year":
                        cat = get_object_or_404(Category,cat_title=categoryName)
                        posts= Post.objects.filter(category=cat.cat_id).filter(post_now=True)
                        post=[]

                        for p in posts :
                            if p.post_date <= date.today():

                                if p.post_date.year==int(year):
                                    post.append(p)
                    else:
                        cat = get_object_or_404(Category,cat_title=categoryName)
                        post= Post.objects.filter(category=cat.cat_id).filter(post_now=True)


            else:
                    allposts= Post.objects.filter(post_now=True)
                    post=[]
                    for p in allposts:
                            if p.post_date <= date.today():
                                posts.append(p)


        except:
                    allposts= Post.objects.filter(post_now=True)
                    post=[]
                    for p in allposts:
                            if p.post_date <= date.today():
                                post.append(p)
        post_year=[]
        post_for_yr= Post.objects.all()
        for p in post_for_yr:

                if p.post_date.year in post_year:
                       pass
                else:
                    post_year.append(p.post_date.year)

        tags= Tag.objects.all()
        paginator = Paginator(post, 6) # Show 25 contacts per page
        category =Category.objects.all()
        ip_count = IpModel.objects.all().count()
        page = request.GET.get('page')
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            post = paginator.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            post = paginator.page(paginator.num_pages)
        context={
            'posts':post,
            'tags':tags,
            'category':category,
            'post_yr':post_year,
            'ip_count':ip_count,
        }
        return render(request,'blog-grid.html',context)

class AddCategoryView(CreateView):
    model= Category
    template_name='editpost.html'
    category=None
    fields = '__all__'
    ip_count = IpModel.objects.all().count()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

class DeletePosttView(DeleteView):
    model = Post
    template_name = 'deletepost.html'
    success_url = reverse_lazy('blog-settings')


class EditPostView(UpdateView):
    model = Post
    template_name = 'editpost.html'
    category= 'true'


    form_class = PostForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

        
class AddPostView(CreateView):
    model = Post
    template_name = 'post.html'
    form_class = PostForm
    success_url = reverse_lazy('blog-settings')

def ContactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request,"Details Saved. We will reach you soon.")
        else:
            #return HttpResponseRedirect(reverse('contact'))
            ip_count = IpModel.objects.all().count()
            #form = ContactForm

            context={
                    'ip_count':ip_count,
                    'form':form
                }
            return render(request,'contact.html',context)
    ip_count = IpModel.objects.all().count()
    form = ContactForm

    context={
            'ip_count':ip_count,
            'form':form
        }
    return render(request,'contact.html',context)

# Create your views here.




def BlogCommentView(request):
    try:
        if User.is_authenticated:
            if request.method == "POST":
                postid = request.POST.get('id')

                if request.POST.get('content')=="":
                    return redirect(f'/blog/{postid}')
                user = request.user
                post = Post.objects.get(post_id=postid)


                content = request.POST.get('content')
            # comment = BlogComment(content=content,user=user,post=post)

                comment = BlogComment(content=content,user=user,post=post)


                comment.save()
             #   messages.success(request,"Your comment has been posted successfully")
            return redirect(f"/blog/{postid}")
        return render(request,'404.html')

    except:
        return render(request,'404.html')


def replaycommentview(request):
    if request.method == "POST":
        pk=request.POST.get('postid')
        commentid = request.POST.get('commentid')
        replay = request.POST.get('content')
        user = request.user

        post =  Post.objects.filter(post_id=pk)
        comment = BlogComment.objects.filter(sno=commentid)

        if replay != ' ':
            comment = ReplayComment(post=post[0],parrent=comment[0],content=replay,user=user)
            comment.save()
            #messages.success(request,"Replay Posted")

        return HttpResponseRedirect(reverse('blog',args=[pk]))
  #  messages.info(request,"not posted")
    return HttpResponseRedirect(reverse('blog',args=[pk]))


















def LikeView(request,pk):

    try:
        # if User.is_authenticated:
        #     post = get_object_or_404(Post,post_id=request.POST.get('post_id'))
        #     if post.like_post.filter(id=request.user.id).exists():
        #         post.like_post.remove(request.user)
        #     else:
        #         post.like_post.add(request.user)
        #     return HttpResponseRedirect(reverse('blog',args=[pk]))
            post = get_object_or_404(Post,post_id=request.POST.get('post_id'))
            ip = get_client_ip(request)
            if not IpModel.objects.filter(ip=ip).exists():
                IpModel.objects.create(ip=ip)
            if post.like_post.filter(id=IpModel.objects.get(ip=ip).id).exists():
                post.like_post.remove(IpModel.objects.get(ip=ip))
            else:
                post.like_post.add(IpModel.objects.get(ip=ip))
            return HttpResponseRedirect(reverse('blog',args=[pk]))

    except :
        return render(request,'404.html')



def HomeView(request):
    ip_count = IpModel.objects.all().count()
    try:
        posts=[]
        all_posts=Post.objects.filter(post_now=True).order_by('-post_date')[:3]
        for post in all_posts:
            if post.post_date <= date.today():
                posts.append(post)
        return render(request,'index.html',{"posts":posts,"ip_count":ip_count})
    except:
         return render(request,'404.html')


def AboutView(request):
    ip_count = IpModel.objects.all().count()

    return render(request,'about.html',{'ip_count':ip_count})
def FQView(request):
    ip_count = IpModel.objects.all().count()

    return render(request,'f&q.html',{'ip_count':ip_count})


def taggedview(request, slug):
    try:
        tag = get_object_or_404(Tag, slug=slug)
        # Filter posts by tag name
        post = Post.objects.filter(tags=tag,post_now=True)
        tags= Tag.objects.all()
        paginator = Paginator(post, 6) # Show 25 contacts per page
        category =Category.objects.all()

        page = request.GET.get('page')
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            post = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            post = paginator.page(paginator.num_pages)
        post_year=[]
        post_for_yr= Post.objects.all()
        print(post_year)
        for p in post_for_yr:

                    if p.post_date.year in post_year:
                           pass
                    else:
                        post_year.append(p.post_date.year)
                        post_year.append(p.post_date.year)
        ip_count = IpModel.objects.all().count()

        context = {
                    'posts':post,
                    'tags':tags,
                    'category':category,
                    'post_yr':post_year,
                    'ip_count':ip_count
            }
        return render(request, 'blog-grid.html', context)
    except:

        return render(request,'404.html')

def searchview(request):
    slug= request.GET.get('search')
    if slug=='':
            messages.warning(request,'Enter Correct word ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        try:
            tag = get_object_or_404(Tag, slug=slug)
            # Filter posts by tag name
            allpost = Post.objects.filter(post_now=True).filter(tags=tag)
            posts=[]
            for post in allpost:
                if post.post_date<=date.today():
                    posts.append(post)
        except:
            try:
                category= get_object_or_404(Category,cat_title=slug)
                posts = Post.objects.filter(category=category, post_now=True)
            except:
                if Post.objects.filter(Q(content__icontains=slug)):
                    posts=Post.objects.filter(Q(content__icontains=slug))
                elif Post.objects.filter(Q(title__icontains=slug)):
                    posts =Post.objects.filter(Q(title__icontains=slug))
                elif Post.objects.filter(Q(writer_name__icontains=slug)):
                    posts=Post.objects.filter(Q(writer_name__icontains=slug))
                else:
                     posts = Post.objects.filter( post_now=True)

        tags= Tag.objects.all()
        ip_count = IpModel.objects.all().count()

        category =Category.objects.all()

        paginator = Paginator(posts, 50) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            post = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            post = paginator.page(paginator.num_pages)
        post_year=[]
        post_for_yr= Post.objects.all()
        for p in post_for_yr:

            if p.post_date.year in post_year:
                   pass
            else:
                post_year.append(p.post_date.year)

        context = {
        'posts':post,
        'tags':tags,
        'category':category,
        'post_yr':post_year,
        'ip_count':ip_count
                }
        return render(request, 'blog-grid.html', context)
            # except:
            #      return render(request,'404.html')



def contactlistView(request):
    context={

    'contavt_detail' : Contact.objects.all(),
    'subsc' : SubcribeUsers.objects.all(),
    'users' : User.objects.all().exclude(is_superuser=True)

    }
    return render(request,'list.html',context)



    # except:
    #     return render(request,'404.html')







def blogsettingsview(request):
    # try:
        posts=Post.objects.all()
        ip_count = IpModel.objects.all().count()
        context={
            'posts':posts,
            'ip_count':ip_count
        }

        return render(request,'preview-blog.html',context,)


def checkbtn(request,pk):
    if  request.method=="POST":
        checked =request.POST.get("check_btn")
        post=get_object_or_404(Post,post_id=pk)
        if checked=='Change':
            post.post_now=False
            post.save()
        else:
            post.post_now=True
            post.save()

        return HttpResponseRedirect(reverse('blog-settings'))

# --------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def subscribeView(request):
    if request.method == "POST":
        email=request.POST.get('email')
        if email !='':
            try :
                memail =SubcribeUsers.objects.get(email=email)
                messages.error(request,'Email Already Register ')

                return HttpResponseRedirect(reverse('blogs'))

            except:

                    form = SubscribeForm(request.POST)
                    if form.is_valid():
                            form.save()

                    messages.success(request,'Subscription Successful')
                    return HttpResponseRedirect(reverse('blogs'))
        else:
                 messages.warning(request,'Enter correct Email id')
                 return HttpResponseRedirect(reverse('blogs'))
    return HttpResponseRedirect(reverse('blogs'))
