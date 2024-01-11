from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Post, UserInfo
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
class newpostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':40, 'placeholder':'Content...'}), min_length=10)

def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-created").all()
    p = Paginator(posts, 10)
    x = request.GET.get("page")
    post = p.get_page(x)
    return render(request, "network/index.html", {
        "form": newpostForm,
        "posts":post,
        "x":1
    })

def newpost(request):
    if request.method == 'POST':
        content = request.POST['content']
        creator = request.user
        if len(content) > 0:
            post = Post.objects.create(creator = creator, content=content)
            post.save()
        return HttpResponseRedirect(reverse("index"))

        
def edit(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        data = json.loads(request.body)
        body = data.get("body", "")
        post.content = body 
        post.save()
        return JsonResponse(f"{post.content}", safe=False)
        # return HttpResponseRedirect(reverse('index'))
    else:
        return JsonResponse('hola', safe=False)

def profile(request, user_id):
    info = UserInfo.objects.get(pk=int(user_id))
    posts = Post.objects.filter(creator=info.user).all()
    posts = posts.order_by("-created").all()
    return  render(request, "network/profile.html",{
        "view":info,
        "posts":posts
    })

def follow(request, user_id):
    u = request.user
    i = User.objects.get(pk=user_id)

    idol = UserInfo.objects.get(user = i)
    fan = UserInfo.objects.get(user = u)

    if u in idol.serialize()['followers']:
        idol.followers.remove(u)
        fan.following.remove(i)
        followers = len(idol.serialize()['followers'])
        following = len(idol.serialize()['following'])
        return JsonResponse({
            "state": "Follow",
            "followers": followers,
            "following": following
        })
    else:
        idol.followers.add(u)
        fan.following.add(i)
        followers = len(idol.serialize()['followers'])
        following = len(idol.serialize()['following'])
        return JsonResponse({
            "state": "Unfollow",
            "followers": followers,
            "following": following
        })
    
def following(request):
    info = UserInfo.objects.get(user=request.user)
    creators =info.serialize()['following'] 
    posts = Post.objects.all
    return render(request, "network/following.html", {
        "posts":posts,
        "creators":creators
    })

def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user not in post.serialize()["likes"]:
        post.likes.add(request.user)
        post.save()
        return JsonResponse(f"{len(post.serialize()['likes'])}", safe=False)
    else:
        post.likes.remove(request.user)
        post.save()
        return JsonResponse(f"{len(post.serialize()['likes'])}", safe=False)

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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            info = UserInfo.objects.create(user=user)
            info.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
