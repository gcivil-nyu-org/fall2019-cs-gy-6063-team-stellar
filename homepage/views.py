from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def index(request):
    if  request.session.get("is_login", None):  # no repeat log in
        return render(request, "homepage.html")
    return redirect("/login")
