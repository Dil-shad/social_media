from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:

        user_profile = None

    return render(request, 'index.html', {'user_profile': user_profile})


def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(
            user=user,
            image=image,
            caption=caption,
        )
        new_post.save()
    return redirect('/')


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
                    user=user_model, id_user=user_model.id)
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
