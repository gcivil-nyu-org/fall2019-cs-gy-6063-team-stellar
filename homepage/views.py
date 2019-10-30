from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    if request.session.get("is_login", None):  # no repeat log in
        return render(request, "homepage.html")
    return redirect("/login/")
