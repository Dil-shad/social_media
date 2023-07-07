from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, LikePost, FollowersCount
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


@login_required(login_url='login')
def index(request):
    try:
        logged_user_profile = get_object_or_404(Profile, user=request.user)
    except:
        logged_user_profile = None

    # retrieving user followed users post

    user_following_profiles = []
    feed_posts = []

    user_following = FollowersCount.objects.filter(
        follower=request.user.username)

    for follower_count in user_following:
        try:
            user_profile = Profile.objects.get(user__username=follower_count)
            user_following_profiles.append(user_profile)
        except ObjectDoesNotExist:
            pass

    for following_profile in user_following_profiles:
        feed_list = Post.objects.filter(Q(user_profile=following_profile) | Q(
            user_profile=logged_user_profile)).order_by('-created_at')
        feed_posts.extend(feed_list)

    # if the user does not follow any other users, show their own posts
    if not feed_posts:
        try:
            feed_posts = Post.objects.filter(
                user_profile=logged_user_profile).order_by('-created_at')
        except:
            feed_posts = []

    return render(request, 'index.html', {'user_profile': logged_user_profile, 'posts': feed_posts})


def follow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST['user']

        user_object = get_object_or_404(User, username=user)

        if FollowersCount.objects.filter(follower=follower, user=user_object).exists():
            delete_follower = FollowersCount.objects.get(
                follower=follower, user=user_object)
            delete_follower.delete()
            return redirect('/profile/' + str(user_object.id))
        else:
            new_follower = FollowersCount(follower=follower, user=user_object)
            new_follower.save()
            return redirect('/profile/' + str(user_object.id))
    return redirect('/')


@login_required(login_url='login')
def ProfileView(request, pk):
    try:
        user_profile = Profile.objects.get(user=pk)
    except Profile.DoesNotExist:
        user_profile = None
    user_posts = Post.objects.filter(user_profile=user_profile).count()
    posts = Post.objects.filter(user_profile=user_profile)

    follower = request.user.username
    user = user_profile
    # print(user_profile)

    # chk weather followed or not
    if FollowersCount.objects.filter(follower=follower, user=user).exists():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = FollowersCount.objects.filter(user=user).count()
    user_following = FollowersCount.objects.filter(follower=user).count()

    context = {'user_profile': user_profile,
               'user_posts': user_posts,
               'posts': posts,
               'button_text': button_text,
               'user_followers': user_followers,
               'user_following': user_following
               }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username)

    if like_filter.exists():
        like_filter.delete()
        post.no_of_likes -= 1
    else:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1

    post.save()
    return redirect('/')


@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        user = user_profile
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(
            user_profile=user,
            image=image,
            caption=caption,
        )
        new_post.save()
    return redirect('index')


@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image')
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        if image:
            user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect('/')
    context = {
        'user_profile': user_profile
    }
    return render(request, 'setting.html', context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        print(password, password2)

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "email already exists")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "username already exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                # log user into the settings page

                user_login = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user_login)

                # creating a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'password not matching')
            return redirect("signup")

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    return render(request, 'signin.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
