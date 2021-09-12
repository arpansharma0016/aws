from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comments
from slugify import slugify

def blog(request):
    blogs = Blog.objects.all()
    context = {
        'blogs':blogs
    }
    return render(request, "blog.html", context)

def blogg(request, id):
    return redirect("blog")


def blog_detail(request, id, name):
    blog = Blog.objects.all()
    bl = get_object_or_404(Blog, id=id)
    li = list()
    com = Comments.objects.filter(post_id=id)
    count = com.count()
    for b in blog:
        if not b.id == id:
            li.append(b)

    context = {
        'blogs':li,
        'blog':bl,
        'comments':com,
        'count':count,
    }
    return render(request, "blog_detail.html", context)


def add_comment(request, id):
    if Blog.objects.filter(id=id).exists():
        bl = Blog.objects.filter(id=id).first()
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            comment = request.POST['comment']
            post_id = id

            com = Comments.objects.create(name=name, email=email, comment=comment, post_id=post_id)
            com.save()

        return redirect("blog_detail", id=id, name=slugify(bl.name))