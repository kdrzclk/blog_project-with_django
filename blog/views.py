from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Like, PostView
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def post_list(request):
    qs = Post.objects.filter(status="published")
    # qs = Post.objects.all()
    # print(qs)
    context = {
        'object_list': qs
    }
    return render(request, 'blog/post_list.html', context)

@login_required()
def post_create(request):
    
    form = PostForm()
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, 'Post Created Succesfully')
            return redirect('blog:list')

    context = {
        'form': form
    }
    return render(request, 'blog/post_create.html', context)

def post_detail(request, slug):
    form = CommentForm()
    obj = get_object_or_404(Post, slug=slug)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=obj)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = obj
            comment.save()

            return redirect("blog:detail", slug=slug)

    context = {
        'object': obj,
        'form': form
    }
    return render(request, 'blog/post_detail.html', context)

def post_update(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
   
    if request.user.id != obj.author.id:
            messages.warning(request, "You aren't a writer of this post. Login or Register please!")
            return redirect('blog:list')

    if form.is_valid():
        form.save()

        messages.success(request, 'Post Updated Succesfully')      
        return redirect("blog:list")
    
    context = {
        'object': obj,
        'form': form
    }
    return render(request, 'blog/post_update.html', context)

def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)

    if request.user.id != obj.author.id:
        messages.warning(request, "You aren't a writer of this post. Login or Register please!")
        return redirect('blog:list')

    if request.method == "POST":
        obj.delete()

        messages.success(request, 'Post Deleted Succesfully')
        return redirect("blog:list")

    context = {
        'object': obj
    }
    return render(request, "blog/post_delete.html", context)

@login_required()
def like(request, slug):
    if request.method == 'POST':
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)

        if like_qs:
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)

        return redirect("blog:detail", slug=slug)
    return redirect("blog:detail", slug=slug)


