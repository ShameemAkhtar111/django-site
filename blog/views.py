from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.views import View
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class StartingView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query[:3]
        return data


# Used the above class based view(StartingView) instead of this method
# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     ## all_posts.sort(key=lambda x : x["date"])
#     # sorted_posts = sorted(all_posts, key=lambda x: x["date"])
#     # latest_posts = sorted_posts[-3:]
#     return render(request, "blog/index.html", context={
#         "posts": latest_posts
#     })


class PostView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "all_posts"
    ordering = ["-date"]


# Used the above class based view (PostView) instead of this method based view
# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {
#         "all_posts":all_posts
#     })


# This below view is only helpful for showing details, but we want to process the form hence uisng View class as base
# class PostDetailsView(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm()
#         return context

class PostDetailsView(View):

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }

        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "blog/post-detail.html", context)


# Used the above class based view (PostDetailsView) instead of this method based view
# def posts_details(request, slug):
#     # identified_post = next(post for post in all_posts if post['slug'] == slug)
#     # identified_post = Post.objects.get(slug=slug)     #same as the below line
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {
#         "post":identified_post,
#         "post_tags": identified_post.tags.all()
#     })