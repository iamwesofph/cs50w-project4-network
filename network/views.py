import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow
from .forms import RegistrationForm


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {'page_obj': page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        last_name = request.POST["last_name"]
        first_name = request.POST["first_name"]
        # profile_pic = request.FILES["profile_pic"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            form = RegistrationForm(request.POST,request.FILES)
            if form.is_valid():
                 # Extract cleaned form data
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                last_name = form.cleaned_data.get('last_name')
                first_name = form.cleaned_data.get('first_name')
                profile_pic = form.cleaned_data.get('profile_pic')

                # Validate data as necessary
                cleaned_handle = form.clean_handle()

                # Create new User object and save it
                user = User.objects.create_user(username=username, email=email, password=password,
                                                last_name=last_name, first_name=first_name, handle=cleaned_handle,
                                                profile_picture=profile_pic)
                user.save()

                # Redirect to success page or login page
                login(request, user)

            else:
                print("form is not valid")
                print(form.errors)
                return render(request, 'network/register.html', {'form': form, 'message':form.errors})

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        return HttpResponseRedirect(reverse("login"))
    else:
        form = RegistrationForm()
        return render(request, "network/register.html", {'form' : form})


@login_required
def tweet(request):

    if request.method == "POST":

        content = request.POST["tweet-content"]   
        post_obj = Post(author=request.user, content=content, created_at=timezone.now())
        post_obj.save()
        return redirect('index')


def profile(request, id):
    user_profile = User.objects.get(pk = id)
    posts = Post.objects.filter(author = user_profile)
    
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user_profile, is_followed=True).exists()
    else:
        is_following = False

    paginator = Paginator(posts, 10)    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {"user_profile" : user_profile, "page_obj" : page_obj, "is_following" : is_following})


@login_required
def following(request):
    followed_users = request.user.following.filter(is_followed=True).values_list("followed", flat=True)
    posts = Post.objects.filter(author__in=followed_users)
    
    paginator = Paginator(posts, 10)    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following.html', {'page_obj': page_obj})


@login_required
def follow(request, id):
    user_to_follow = get_object_or_404(User, id=id)

    try:
        # check if the current user is already following the followed user
        follow = Follow.objects.get(follower=request.user, followed=user_to_follow)
        if request.POST['action'] == 'unfollow':
            follow.is_followed = False
            follow.save()
        elif request.POST['action'] == 'follow':
            follow.is_followed = True
            follow.save()
    except Follow.DoesNotExist:
        # if there is no Follow object, create a new one to follow the user
        follow = Follow.objects.create(follower=request.user, followed=user_to_follow, is_followed=True)

    # redirect to the user's profile page
    return redirect('profile', id=id)


@csrf_exempt
def update(request, id):

    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        # return JsonResponse({'message': 'Post updated successfully'})
        return JsonResponse({'message': 'Post updated successfully', 'content': post.content})


@csrf_exempt
def like(request, post_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post_id = data.get("post_id")

    # Confirm validity of user and post id
    try:
        user = request.user
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({ "error": f"Post with id {post_id} does not exist."}, status=400)

    # Check if like object exists (if user liked the post before but unliked it)
    try:
        like_o = Like.objects.get(post=post, user=user)
        # Toggle the status of is_like if record exists
        if like_o.is_like:
            like_o.is_like = False
        else:
            like_o.is_like = True
        like_o.save()
    except Like.DoesNotExist:
        Like.objects.create(post=post, user=user, is_like=True)

    return JsonResponse({"message": "Liked successfully."}, status=201)
