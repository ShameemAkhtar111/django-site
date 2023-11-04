from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def starting_page(request):
    return render(request, "blog/index.html")


def posts(request):
    return render(request, "blog/all-posts.html")


def posts_details(request):
    pass