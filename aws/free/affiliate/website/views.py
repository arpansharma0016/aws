from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from accounts.models import Product, Visitor_counter, Info, Banner, Widget, Tag
import datetime
import random
from django.contrib.humanize.templatetags.humanize import intcomma
from slugify import slugify





def dynamic(request, username):
    obj = get_object_or_404(User, username=username)
    p = Product.objects.filter(username=username)
    obj2 = User.objects.get(username=username)
    
    visitor = Visitor_counter.objects.get(username=username)
    number = visitor.counter
    if request.user.is_authenticated:
        if obj.username == request.user.username:
            number = number
        else:
            number = number + 1
    else:
        number = number + 1
    visitor.counter = number
    visitor.save()

    ca = Product.objects.filter(username = username)
    category = ca.all()
    uo = Product.objects.filter(username = username)
    userpro = uo.all()
    user_info = Info.objects.get(username = username)
    li = list()
    if not category:
        bro = False
                
    yoyo = 0
    yoyoyo = 0
    for cat in category:
        if cat.product_category not in li:
            bro = True
            li.append(cat.product_category)
            
    cat_pro_ctr=0
    leng = len(li) 
    product = p.all()
    widget = Widget.objects.filter(username=username)
    banner = Banner.objects.filter(username=username)
    tag = Tag.objects.filter(username=username)
    for t in tag:
        tag = t
    context = {
        "object":obj,
        "pro":product,
        "li":li,
        "bro":bro,
        "userpro":userpro,
        "yoyo":yoyo,
        "leng":leng,
        "cat_pro_ctr":cat_pro_ctr,
        "user_info":user_info,
        "yoyoyo":yoyoyo,
        "banner":banner,
        "widget":widget,
        'tag':tag,
    }
    
    return render(request, "site.html", context)
    
def product(request, username, pro_id, product_slug):
    pro = get_object_or_404(Product, id=pro_id)
    if pro:
        visitor = Visitor_counter.objects.get(username=username)
        number = visitor.product_counter
        if request.user.is_authenticated:
            if username == request.user.username:
                number = number
            else:
                number += 1
        else:
            number += 1
        visitor.product_counter = number
        visitor.save()
        product_user = Product.objects.filter(username=username)
        user_name = ""
        for pro_us in product_user:
            user_name = pro_us.username
        if user_name == pro.username:
            category = Product.objects.filter(username=username)
            ca = Product.objects.filter(product_category=pro.product_category).filter(username=username).order_by('?')
            
            li = list()
            if not category:
                bro = False
                        
            yoyo = 0
            yoyoyo = 0
            for cat in category:
                if cat.product_category not in li:
                    bro = True
                    li.append(cat.product_category)
            leng = len(li)

            diction = {}
            ctr=0
            for list_item in li:
                for apj in category:
                    if apj.product_category == list_item:
                        ctr += 1
                diction[list_item] = ctr
                ctr=0
            user_info = Info.objects.get(username=username)
            widget = Widget.objects.filter(username=username)
            banner = Banner.objects.filter(username=username)
            context = {
                "pro":pro,
                "category":category,
                "li":li,
                "leng":leng,
                "diction":diction,
                "ca":ca,
                "banner":banner,
                "widget":widget,
                "user_info":user_info

            }

            return render(request, "product_page.html", context)

        else:
            return redirect("dynamic" , pro.username)

        
        
