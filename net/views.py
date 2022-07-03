from calendar import c
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
import pytz
import tzlocal
import json
from django.http import JsonResponse
from .models import User, Post, Comment, Profile
from django.db import IntegrityError
from django import forms
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


class PostForm(forms.Form):
    description = forms.CharField(label='', widget=forms.Textarea(attrs={f'placeholder': "What's on your mind?", 'class': 'index-textarea'}))

class CommentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Post a comment here...', 'class': 'post-comment-textarea', 'autofocus': 'autofocus'}))
    
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']

def time_for_queryset(request, post):
    date = post.date_posted
    local_timezone = tzlocal.get_localzone()
    new_date = date.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    difference = datetime.datetime.now() - new_date.replace(tzinfo=None)

    if difference.total_seconds() > 60:
        minutes = difference.total_seconds() / 60
        if minutes > 60:
            hours = difference.total_seconds() / 60**2
            if hours > 24:
                if difference.days > 7:
                    weeks = difference.days / 7
                    if weeks > 4:
                        month = weeks / 4
                        if month > 12:
                            year = difference.days / 365
                            post.date_posted = f"{int(year)}y ago"
                        else:
                            post.date_posted = f"{int(month)}m ago"
                    else:
                        post.date_posted = f"{int(weeks)}w ago"
                else:
                    post.date_posted = f"{int(difference.days)}d ago"
            else:
                post.date_posted = f"{int(hours)}h ago"
        else:
            post.date_posted = f"{int(minutes)}m ago"
    else:
        post.date_posted = f"{int(difference.total_seconds())}s ago"

    return post

def calculate_time(request, posts):
    for post in posts:
        date = post.date_posted
        local_timezone = tzlocal.get_localzone()
        new_date = date.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        difference = datetime.datetime.now() - new_date.replace(tzinfo=None)

        if difference.total_seconds() > 60:
            minutes = difference.total_seconds() / 60
            if minutes > 60:
                hours = difference.total_seconds() / 60**2
                if hours > 24:
                    if difference.days > 7:
                        weeks = difference.days / 7
                        if weeks > 4:
                            month = weeks / 4
                            if month > 12:
                                year = difference.days / 365
                                post.date_posted = f"{int(year)}y ago"
                            else:
                                post.date_posted = f"{int(month)}m ago"
                        else:
                            post.date_posted = f"{int(weeks)}w ago"
                    else:
                        post.date_posted = f"{int(difference.days)}d ago"
                else:
                    post.date_posted = f"{int(hours)}h ago"
            else:
                post.date_posted = f"{int(minutes)}m ago"
        else:
            post.date_posted = f"{int(difference.total_seconds())}s ago"
    return posts

import operator

@login_required(login_url='/login')    
def index(request):

    store_posts = []
    followings_list = request.user.followings.all()
    posts = request.user.posts.all().order_by('-date_posted')
    for user in followings_list:
        store_posts += user.posts.all()
    store_posts += posts

    sort_posts = sorted(store_posts, key=operator.attrgetter('date_posted'), reverse=True)

    p = Paginator(sort_posts, 10)
    page = request.GET.get('page')
    posts_paginated =  p.get_page(page)
    num_of_pages = 'p' * posts_paginated.paginator.num_pages
    
    
    context = {
        'post_form': PostForm(),
        'posts_paginated': calculate_time(request, posts_paginated),
        'num_of_pages': num_of_pages,
        'sort_posts': sort_posts
    }

    if request.method == 'POST':
        form = PostForm(request.POST)

        if 'index-follow-id' in request.POST:
            index_follow_id = int(request.POST['index-follow-id'])
            index_follow_instance = User.objects.get(id=index_follow_id)

        if 'layout-follow-id' in request.POST:
            layout_follow_id = int(request.POST['layout-follow-id'])
            layout_instance = User.objects.get(id=layout_follow_id)

        if form.is_valid():
            desc = form.cleaned_data['description']
            save_post = Post(description=desc, user=request.user, date_posted=datetime.datetime.utcnow())
            save_post.save()
            return redirect('index')

        if request.POST.get('delete-post') == 'Delete Post':
            hidden_id = int(request.POST['delete_postid'])
            post_obj = Post.objects.get(id=hidden_id)
            post_obj.delete()
            return redirect('index')

        elif request.POST.get('index-unfollow') == 'Unfollow':
            index_follow_instance.follower.remove(request.user)
            request.user.followings.remove(index_follow_instance)
            return redirect('index')

        elif request.POST.get('index-follow') == 'Follow':
            index_follow_instance.follower.add(request.user)
            request.user.followings.add(index_follow_instance)
            return redirect('index')

        elif request.POST.get('layout-follow') == 'Follow':
            layout_instance.follower.add(request.user)
            request.user.followings.add(layout_instance)

            # Redirect the user to the page they are on
            return redirect(request.META['HTTP_REFERER'])

    return render(request, 'net/index.html', context)


@login_required(login_url='/login')
def single_post_view(request, post_id):
    
    try:
        post_obj = Post.objects.get(id=post_id)
        post_comments = post_obj.comments.all().order_by('-date_posted')
    except Post.DoesNotExist:
        return render(request, "net/error.html", {
            "error_msg": "The requested post does not exist."
        }) 
    
    p = Paginator(calculate_time(request, post_comments), 10)
    page = request.GET.get('page')
    comments_paginated =  p.get_page(page)
    num_of_pages = 'p' * comments_paginated.paginator.num_pages

    context = {
        'comment_form': CommentForm(),
        'post_obj': time_for_queryset(request, post_obj),
        'comments_paginated': comments_paginated,
        'num_of_pages': num_of_pages,
        'comments_num': len(post_comments)
    }

    if request.method == "POST":
        if 'post-view-follow-id' in request.POST:
            post_view_id = int(request.POST['post-view-follow-id'])
            post_view_instance = User.objects.get(id=post_view_id)

        if 'post-comment-follow-id' in request.POST:
            post_comment_follow_id = int(request.POST['post-comment-follow-id'])
            post_comment_follow_ins = User.objects.get(id=post_comment_follow_id)

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.cleaned_data['comment']
            save_comment = Comment(post=post_obj, user=request.user, comment=comment, date_posted=datetime.datetime.utcnow())
            save_comment.save()
            return redirect(f'/post/{post_id}')
            
        if request.POST.get('post-view-unfollow') == 'Unfollow':
            post_view_instance.follower.remove(request.user)
            request.user.followings.remove(post_view_instance)
            return redirect(f'/post/{post_id}')

        elif request.POST.get('post-view-follow') == 'Follow':
            post_view_instance.follower.add(request.user)
            request.user.followings.add(post_view_instance)
            return redirect(f'/post/{post_id}')

        elif request.POST.get('post-view-delete-post') == 'Delete Post':
            hidden_id = int(request.POST['post-view-delete_postid'])
            post_obj = Post.objects.get(id=hidden_id)
            post_obj.delete()
            return redirect('index')

        elif request.POST.get('delete-comment') == 'Delete':
            delete_comment_id = int(request.POST['delete_comment_id'])
            delete_comment_ins = Comment.objects.get(id=delete_comment_id)
            delete_comment_ins.delete()
            return redirect(f'/post/{post_id}')

        elif request.POST.get('post-comment-unfollow') == 'Unfollow':
            post_comment_follow_ins.follower.remove(request.user)
            request.user.followings.remove(post_comment_follow_ins)
            return redirect(f'/post/{post_id}')

        elif request.POST.get('post-comment-follow') == 'Follow':
            post_comment_follow_ins.follower.add(request.user)
            request.user.followings.add(post_comment_follow_ins)
            return redirect(f'/post/{post_id}')

    return render(request, 'net/post.html', context)


@login_required(login_url='/login')
def profile(request, user_id):

    try:
        user_profile = User.objects.get(id=user_id)
        user_profile_posts = user_profile.posts.all().order_by('-date_posted')
    except User.DoesNotExist:
        return render(request, "net/error.html", {
            "error_msg": "The requested user does not exist."
        }) 

    p = Paginator(user_profile_posts, 10)
    page = request.GET.get('page')
    posts_paginated = p.get_page(page)
    num_of_pages = "p" * posts_paginated.paginator.num_pages

    context = {
        'user_profile': user_profile,
        'posts_paginated': calculate_time(request, posts_paginated),
        'num_of_pages': num_of_pages,
        'followers': user_profile.follower.all(),
        'followings': user_profile.followings.all(),
        'profile_form': ProfilePictureForm()
    }

    if request.method == 'POST':
        if 'profile-follow-id' in request.POST:
            profile_view_id = int(request.POST['profile-follow-id'])
            profile_view_instance = User.objects.get(id=profile_view_id)
            
        if 'profile-delete_postid' in request.POST:
            hidden_id = int(request.POST['profile-delete_postid'])
            post_obj = Post.objects.get(id=hidden_id)

        if request.POST.get('update-image') == 'Update':
            profile_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect(f'/profile/{user_id}')

        elif request.POST.get('profile-follow') == 'Follow':
            profile_view_instance.follower.add(request.user)
            request.user.followings.add(profile_view_instance)
            return redirect(f'/profile/{user_id}')

        elif request.POST.get('profile-unfollow') == 'Unfollow':
            profile_view_instance.follower.remove(request.user)
            request.user.followings.remove(profile_view_instance)
            return redirect(f'/profile/{user_id}')

        elif request.POST.get('profile-delete-post') == 'Delete Post':
            post_obj.delete()
            return redirect(f'/profile/{user_id}')

    return render(request, 'net/profile.html', context)


@login_required(login_url='/login')
def suggestions(request):
    exclude_user = User.objects.exclude(username=request.user)
    store_non_followings = []

    if request.method == 'POST':
        if 'suggestion-id' in request.POST:
            suggestion_id = int(request.POST['suggestion-id'])
            suggestion_instance = User.objects.get(id=suggestion_id)

        if request.POST.get('suggestion-follow') == 'Follow':
            suggestion_instance.follower.add(request.user)
            request.user.followings.add(suggestion_instance)
            return redirect('suggestions')

    context = {}
    for user in exclude_user:
        if user not in request.user.followings.all():
            store_non_followings.append(user)
            context['non_followings'] = store_non_followings

    return render(request, 'net/suggestions.html', context)


@login_required(login_url='/login')
def suggestions_api(request):
    exclude_user = User.objects.exclude(username=request.user)
    store_non_followings = []

    for user in exclude_user:
        if user not in request.user.followings.all():
            store_non_followings.append(user.serialize())

    return JsonResponse(store_non_followings, safe=False)


@login_required(login_url='/login')
def follow(request, user_id):
    try:
        instance = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, "net/error.html", {
            "error_msg": "The requested user does not exist."
        }) 

    data = int(json.loads(request.body)['follower'])

    # Check if data was tamepered with
    if request.user.id == data:
        current_user = User.objects.get(id=data)

        if current_user not in instance.follower.all():
            instance.follower.add(current_user)
            current_user.followings.add(instance)
        else:
            instance.follower.remove(current_user)
            current_user.followings.remove(instance)
    else: 
        return render(request, "net/error.html", {
            "error_msg": "Request aborted!. You tried accessing forbidden data."
        }) 

    return JsonResponse(instance.serialize(), safe=False)
    

@login_required(login_url='/login')
def editPost(request, post_id):

    try:
        posts = Post.objects.get(user=request.user, id=post_id)
    except Post.DoesNotExist:
        return render(request, "net/error.html", {
            "error_msg": "Requested aborted! You tried accessing a forbidden post. "
        }) 

    posts.description = json.loads(request.body)['description']
    posts.save()

    return JsonResponse(posts.serialize(), safe=False)


@login_required(login_url='/login')
def likePost(request, post_id):
    try:
        posts = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return render(request, "net/error.html", {
            "error_msg": "The requested post does not exist."
        }) 

    if request.method == "PUT":
        data = int(json.loads(request.body)['likes'])

        if request.user.id == data:
            if request.user in posts.likes.all():
                posts.likes.remove(request.user.id)
            else:
                posts.likes.add(request.user.id)
        else:
            return render(request, "net/error.html", {
                "error_msg": "Request aborted!. You tried accessing forbidden data."
            }) 

    return JsonResponse(posts.serialize(), safe=False)



@login_required(login_url='/login')
def likeComment(request, comment_id):
    try:
        comments = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return render(request, "net/error.html", {
            "error_msg": "The requested comment does not exist."
        }) 

    if request.method == 'PUT':
        data = int(json.loads(request.body)['likes'])

        if request.user.id == data:
            if request.user in comments.likes.all():
                comments.likes.remove(request.user.id)
            else:
                comments.likes.add(request.user.id)
        else:
            return render(request, "net/error.html", {
                "error_msg": "Request aborted!. You tried accessing forbidden data."
            }) 

    return JsonResponse(comments.serialize(), safe=False)


@login_required(login_url='/login')
def followings_page(request, user_id):
    try: 
        instance = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, "net/error.html", {
            "error_msg": "The requested user does not exist."
        }) 

    user_followings = instance.followings.all()


    if request.method == 'POST':
        following_id = int(request.POST['following-id'])
        following_instance = User.objects.get(id=following_id)

        if request.POST.get('unfollow') == 'Unfollow':
            following_instance.follower.remove(request.user)
            request.user.followings.remove(following_instance)
            return redirect(f'/profile/{user_id}/followings')

        elif request.POST.get('follow') == 'Follow':
            following_instance.follower.add(request.user)
            request.user.followings.add(following_instance)
            return redirect(f'/profile/{user_id}/followings')

    context = {
        'all_user_followings' : user_followings,
        'user_instance': instance
    }
    return render(request, 'net/followings_page.html', context)

@login_required(login_url='/login')
def followings_page_api(request, user_id):
    try:
        instance = User.objects.get(id=user_id)
        all_followings = instance.followings.all()
    except User.DoesNotExist:
        return render(request, 'net/error.html', {
            'error_msg': 'The requested user does not exist.'
        })

    data = []
    for i in all_followings:
        data.append(i.serialize())
    return JsonResponse({'all_user_followings': data})


@login_required(login_url='/login')
def followers_page(request, user_id):
    try: 
        instance = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, "net/error.html", {
            "error_msg": "The requested user does not exist."
        }) 

    user_followers = instance.follower.all()

    if request.method == 'POST':
        follower_id = int(request.POST['follower-id'])
        follower_instance = User.objects.get(id=follower_id)

        if request.POST.get('follow') == 'Follow':
            follower_instance.follower.add(request.user)
            request.user.followings.add(follower_instance)
            return redirect(f'/profile/{user_id}/followers')

        elif request.POST.get('unfollow') == 'Unfollow':
            follower_instance.follower.remove(request.user)
            request.user.followings.remove(follower_instance)
            return redirect(f'/profile/{user_id}/followers')
    context = {
        'all_user_followers': user_followers,
        'user_instance': instance
    }

    return render(request, 'net/followers_page.html', context)


@login_required(login_url='/login')
def followers_page_api(request, user_id):
    try:
        instance = User.objects.get(id=user_id)
        all_followers = instance.follower.all()
    except User.DoesNotExist:
        return render(request, "net/error.html", {
            "error_msg": "The requested user does not exist."
        }) 

    data = []
    for i in all_followers:
        data.append(i.serialize())

    return JsonResponse({'all_user_followers': data})


@login_required(login_url='/login')
def error_handling(request):
    return render(request, 'net/error.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        if password != confirmation:
            return render(request, "net/register.html", {
                "message": "Passwords do not match."
            })
        if username == '':
            return render(request, "net/register.html", {
                "message": "Username field cannot be blank"
            })
        if email == '':
            return render(request, "net/register.html", {
                "message": "Email field cannot be blank."
            })
        if password == '':
            return render(request, "net/register.html", {
                "message": "Password field cannot be blank."
            })
        if confirmation == '':
            return render(request, "net/register.html", {
                "message": "Confirmation field cannot be blank."
            })
        all_users = User.objects.all()

        for u in all_users:
            if username == u.username:
                return render(request, "net/register.html", {
                    "message": "Username already taken."
                })
            elif email == u.email:
                return render(request, "net/register.html", {
                    "message": "Email already taken."
                })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "net/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('index')
    else:
        return render(request, "net/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'net/login.html', {
                'message': 'Invalid username and/or password.'
            })
    return render(request, "net/login.html")

def logout_view(request):
    logout(request)
    return redirect('index')
