from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import Post, Comment, Upvoter

def check_show_upvote(request, post):
    ret = False
    try:
        post.upvoter_set.get(username = request.user.username)
    except (KeyError, Upvoter.DoesNotExist):
        ret = True
    else:
        ret = False

    if not request.user.is_authenticated:
        ret = False
    return ret

def add_post_execute(request):
    print(request.POST)
    title = request.POST['title']
    content = request.POST['new_content']
    pub_date = timezone.now()
    post = Post.objects.create(content = content, title = title, pub_date = pub_date)
    return HttpResponseRedirect(reverse('blog:index'))

class add_post(CreateView):
    model = Post
    template_name = 'blog/add_post.html'
    fields = ('title', 'content')

def index(request):
    latest_post_list = Post.objects.order_by("-pub_date")[0:10]
    return render(request, 'blog/index.html', {
        'latest_post_list': latest_post_list,
    })

def detail(request, post_id):
    post = Post.objects.get(id = post_id)
    comment_list = post.comment_set.all()
    upvoter_list = post.upvoter_set.all()
    user = request.user
    show_upvote = check_show_upvote(request, post)
    if request.method == 'POST':
        post.upvotes += 1
        post.save()
        post.upvoter_set.create(username = user.username)
        return HttpResponseRedirect(reverse('blog:detail', args = (post_id, )))
    else:
        return render(request, 'blog/detail.html', {
            'post_id': post_id,
            'post': post,
            'comment_list': comment_list,
            'show_upvote': show_upvote,
        })

def contact_view(request):
    return render(request, 'blog/contact.html', {

    })

def post_comment(request, post_id):
    user = request.user
    new_comment = request.POST['comment']
    post = Post.objects.get(id = post_id)
    comment_list = post.comment_set.all()
    if new_comment:
        post.comment_set.create(pub_date = timezone.now(), content = new_comment, user = user.username)
        return HttpResponseRedirect(reverse('blog:detail', args = (post_id, )))
    else:
        error_message = "Your comment cannot be an empty comment!"
        show_upvote = check_show_upvote(request, post)
        return render(request, 'blog/detail.html', {
            'post': post,
            'post_id': post_id,
            'comment_list': comment_list,
            'show_upvote': show_upvote,
            'error_message': error_message,
        })

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            messages.success(request, ("There was an Error Logging In, Try Again..."))
            return HttpResponseRedirect(reverse('blog:login'))
    else:
        return render(request, 'blog/login.html', {})

def signup_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        re_password = request.POST['re_password']
        full_name = request.POST['full_name']
        if password == re_password:
            user = User.objects.create_user(username = username, password = password, first_name = full_name)
            user.save()
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            error_message = 'Your passwords did not match!'
            return render(request, 'blog/signup.html', {
                'error_message': error_message,
            })
    else:
        return render(request, 'blog/signup.html', {})

def logout_user(request):
    logout(request);
    return HttpResponseRedirect(reverse('blog:index'))

def edit_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id = comment_id)
    post = Post.objects.get(id = post_id)
    return render(request, 'blog/edit_comment.html', {
        'post': post,
        'comment': comment,
    })

def update_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id = comment_id)
    post = Post.objects.get(id = post_id)
    error_message = "Please type an actual comment before pressing update"
    if request.POST['edited_comment']:
        comment.content = request.POST['edited_comment']
        comment.save()
    else:
        return render(request, 'blog/edit_comment.html', {
            'error_message': error_message,
        })
    return HttpResponseRedirect(reverse("blog:detail", args = (post_id, )))

def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id = comment_id)
    comment.delete()
    return HttpResponseRedirect(reverse('blog:detail', args = (post_id, )))
