from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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
    vi_id = visitor.id
    if request.user.is_authenticated:
        if obj.username == request.user.username:
            new_counter = number
        else:
            new_counter = number + 1
    else:
        new_counter = number + 1
    uname = visitor.username
    visitor.delete()
    new = Visitor_counter.objects.create(id=vi_id,username=uname,counter=new_counter)
    new.save()
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
    paid_user = Info.objects.get(username=username)
    if paid_user.paid:

        day_of_subscription = int(paid_user.day_of_subscription)
        day_of_expiry = int(paid_user.day_of_expiry)
        month_of_subscription = paid_user.month_of_subscription
        month_of_expiry = paid_user.month_of_expiry
        if month_of_expiry == "January":
            month_ox = 1
        if month_of_expiry == "February":
            month_ox = 2
        if month_of_expiry == "March":
            month_ox = 3
        if month_of_expiry == "April":
            month_ox = 4
        if month_of_expiry == "May":
            month_ox = 5
        if month_of_expiry == "June":
            month_ox = 6
        if month_of_expiry == "July":
            month_ox = 7
        if month_of_expiry == "August":
            month_ox = 8
        if month_of_expiry == "September":
            month_ox = 9
        if month_of_expiry == "October":
            month_ox = 10
        if month_of_expiry == "November":
            month_ox = 11
        if month_of_expiry == "December":
            month_ox = 12
        year_of_subscription = int(paid_user.year_of_subscription)
        year_of_expiry = int(paid_user.year_of_expiry)

        expiry = datetime.datetime(year_of_expiry, month_ox, day_of_expiry)
        date_today = datetime.datetime.now()
        if date_today > expiry:
            paid_user.paid = False
            paid_user.save()
            return HttpResponse("The Site Owner's Subscription Period Has Expired. Once The Subscription Is Re-initiated, The Products Will Reappear")
        else:
            return render(request, "site.html", context)
    else:
        return HttpResponse("The Site Owner's Subscription Period Has Expired. Once The Subscription Is Re-initiated, The Products Will Reappear")
    
    
    
    
def product(request, username, pro_id, product_slug):
    paid_user = get_object_or_404(Info, username=username)
    if paid_user.paid:

        day_of_subscription = int(paid_user.day_of_subscription)
        day_of_expiry = int(paid_user.day_of_expiry)
        month_of_subscription = paid_user.month_of_subscription
        month_of_expiry = paid_user.month_of_expiry
        if month_of_expiry == "January":
            month_ox = 1
        if month_of_expiry == "February":
            month_ox = 2
        if month_of_expiry == "March":
            month_ox = 3
        if month_of_expiry == "April":
            month_ox = 4
        if month_of_expiry == "May":
            month_ox = 5
        if month_of_expiry == "June":
            month_ox = 6
        if month_of_expiry == "July":
            month_ox = 7
        if month_of_expiry == "August":
            month_ox = 8
        if month_of_expiry == "September":
            month_ox = 9
        if month_of_expiry == "October":
            month_ox = 10
        if month_of_expiry == "November":
            month_ox = 11
        if month_of_expiry == "December":
            month_ox = 12
        year_of_subscription = int(paid_user.year_of_subscription)
        year_of_expiry = int(paid_user.year_of_expiry)

        expiry = datetime.datetime(year_of_expiry, month_ox, day_of_expiry)
        date_today = datetime.datetime.now()
        if date_today > expiry:
            paid_user.paid = False
            paid_user.save()
            return HttpResponse("The Site Owner's Subscription Period Has Expired. Once The Subscription Is Re-initiated, The Products Will Reappear")
        else:
            pro = get_object_or_404(Product, id=pro_id)
            if pro:
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

        
        
        
        
        

    
    







