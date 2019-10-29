from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def index(request):
    if not request.session.get("is_login", None):  # no repeat log in
        return redirect("/login")
    return render(request, "homepage.html")