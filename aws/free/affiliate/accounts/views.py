from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Product, Visitor_counter, Info, Confirm, Password, Banner, Widget, Tag
from homepage.models import Newsletter
import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import random
import math
from django.contrib.auth.hashers import make_password




def register(request):
    
    if request.method == 'POST':
        if not request.POST['first_name']:
            messages.info(request, "Please enter your name!")
            return redirect("register")
        first_name = request.POST['first_name']

        if not request.POST['username']:
            messages.info(request, "Please enter your username!")
            return redirect("register")
        username = request.POST['username']
        
        if not request.POST['password1']:
            messages.info(request, "Please enter your password!")
            return redirect("register")
        password1 = request.POST['password1']
        
        if not request.POST['password2']:
            messages.info(request, "Please enter your password!")
            return redirect("register")
        password2 = request.POST['password2']
        
        if not request.POST['email']:
            messages.info(request, "Please enter your email!")
            return redirect("register")
        email = request.POST['email']
        
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect("register")
            
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect("register")
            
            elif "." in username:
                messages.info(request, 'Username must not contain " . " ')
                return redirect("register")
            
            else:
                for i in username:
                    if i.isupper():
                        messages.info(request, 'Username must be lowercase')
                        return redirect("register")
                        
                    else:
                        if Confirm.objects.filter(username=username).exists():
                            confirm_user = Confirm.objects.get(username=username)
                            confirm_user.delete()
                            digits = "0123456789"
                            otp = ""
                            for i in range(6):
                                otp += digits[math.floor(random.random()*10)]
                            new_otp = otp
                            confirm_user = Confirm.objects.create(username=username, name=first_name, email=email, password=password1, otp=new_otp)
                            confirm_user.save()
                            subject = 'Thank You for registering to Affiliator!'
                            message = 'Hi ' + confirm_user.name + '!\n \nWe have recieved an Account Creation request from you.\n\nYour Email Confirmation Code is '+new_otp+'.\n\nAt Affiliator, you can easily add Affiliate Products right from your Dedicated Dashboard. Some key features are\n1) No Coding Required\n2) 100% Mobile Responsive\n3) Unlimitted Affiliate Products\n4) Unlimitted Bandwidth\n5) Add Unlimitted Product Categories\n6) Edit any Product Detail\nand many more...\n\nOur Dedicated Management Team is always at your service in case of any Discrepency\nAll the Best\nTeam Affiliator.'
                            from_email = settings.EMAIL_HOST_USER
                            to_list = [confirm_user.email]
                            send_mail(subject, message, from_email, to_list, fail_silently=True)
                            messages.info(request, "An Account Confirmation email has been sent to "+confirm_user.email+". Please Enter the code here.")
                            return redirect("confirm_email", username)
                        else:
                            digits = "0123456789"
                            otp = ""
                            for i in range(6):
                                otp += digits[math.floor(random.random()*10)]
                            new_otp = otp
                            confirm_user = Confirm.objects.create(username=username, name=first_name, email=email, password=password1, otp=new_otp)
                            confirm_user.save()
                            subject = 'Thank You for registering to Affiliator!'
                            message = 'Hi ' + confirm_user.name + '!\n \nWe have recieved an Account Creation request from you.\n\nYour Email Confirmation Code is '+new_otp+'.\n\nAt Affiliator, you can easily add Affiliate Products right from your Dedicated Dashboard. Some key features are\n1) No Coding Required\n2) 100% Mobile Responsive\n3) Unlimitted Affiliate Products\n4) Unlimitted Bandwidth\n5) Add Unlimitted Product Categories\n6) Edit any Product Detail\nand many more...\n\nOur Dedicated Management Team is always at your service in case of any Discrepency\nAll the Best\nTeam Affiliator.'
                            from_email = settings.EMAIL_HOST_USER
                            to_list = [confirm_user.email]
                            send_mail(subject, message, from_email, to_list, fail_silently=True)
                            messages.info(request, "An Account confirmation email has been sent to "+confirm_user.email)
                            return redirect("confirm_email", username)
        
        else:
            messages.info(request, 'Passwords dont match')
            return redirect("register")
        
    else:
        return render(request, 'register.html')

def confirm_email(request, uname):
    
    if not Confirm.objects.filter(username=uname).exists():
        messages.info(request, "Please register first")
        return redirect("register")
    else:
        confirm_email = Confirm.objects.get(username=uname)
        old_otp = confirm_email.otp
        
        if request.method == 'POST':
            if not request.POST['confirm']:
                messages.info(request, "Please enter the OTP sent to your email address!")
                return redirect("confirm_email", uname)
            otp = request.POST['confirm']
            if otp == old_otp:
                user = User.objects.create_user(username=confirm_email.username, password=confirm_email.password, first_name=confirm_email.name, email=confirm_email.email)
                ctr = Visitor_counter.objects.create(username=confirm_email.username)
                apj = Info.objects.create(username=confirm_email.username)
                email_save = Newsletter.objects.create(email=confirm_email.email)
                email_save.save()
                apj.save()
                ctr.save()
                user.save()
                confirm_email.delete()
                messages.info(request, "Email confirmed successfully!")
                messages.info(request, "Login to continue.")
                return redirect("login")
            else:
                if confirm_email.attempts < 4:
                    confirm_email.attempts +=1
                    confirm_email.save()
                    messages.info(request, "Incorrect Otp, Try Again.")
                    messages.info(request, str((5-confirm_email.attempts))+ " attempts left.")
                    return redirect("confirm_email", uname)
                else:
                    confirm_email.attempts = 0
                    confirm_email.save()
                    messages.info(request, "Maximum Attempts held for this confirmation code. We've sent a new Confirmation code to "+confirm_email.email+". Please enter the new Code.")
                    return redirect("resend_code", confirm_email.username)

        

        return render(request, "confirm_email.html", {'confirm_email':confirm_email})


def resend_code(request, uname):
    if Confirm.objects.filter(username=uname).exists():
        confirm_user = Confirm.objects.get(username=uname)
        digits = "0123456789"
        otp = ""
        for i in range(6):
            otp += digits[math.floor(random.random()*10)]
        new_otp = otp
        confirm_user.otp = new_otp
        confirm_user.save()
        subject = 'Your new Password Confirmation Code is '+new_otp+'.'
        message = 'Hi ' + confirm_user.name + '!\n \nWe have recieved an Account Creation request from you.\n\nYour New Email Confirmation Code is '+new_otp+'.\n\nAt Affiliator, you can easily add Affiliate Products right from your Dedicated Dashboard. Some key features are\n1) No Coding Required\n2) 100% Mobile Responsive\n3) Unlimitted Affiliate Products\n4) Unlimitted Bandwidth\n5) Add Unlimitted Product Categories\n6) Edit any Product Detail\nand many more...\n\nOur Dedicated Management Team is always at your service in case of any Discrepency\nAll the Best\nTeam Affiliator.'
        from_email = settings.EMAIL_HOST_USER
        to_list = [confirm_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        messages.info(request, "Account confirmation email has been sent to "+confirm_user.email)
        return redirect("confirm_email", uname)
    else:
        messages.info(request, "Please register first!")
        return redirect("register")
    




def login(request):
    
    if request.method == 'POST':
        if not request.POST['username']:
            messages.info(request, "Invalid Credentials!")
            return redirect("login")
        username = request.POST['username']
        
        if not request.POST['password']:
            messages.info(request, "Invalid Credentials!")
            return redirect("login")
        password = request.POST['password']
        for i in username:
            if i.isupper():
                messages.info(request, 'Username must be lowercase')
                return redirect("login")
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            confirm_user = User.objects.get(username=username)
            subject = 'New login activity on your Affiliator account!'
            message = 'Hi ' + confirm_user.first_name + '!\n \nHope you are having a great time with Affiliator Affiliate Management Program.\n\nWe have detected a new login activity to your Affiliator Account with following details:-\nDate :- '+datetime.datetime.now().strftime("%d")+' '+datetime.datetime.now().strftime("%B")+' '+datetime.datetime.now().strftime("%Y")+'\nTime :- '+datetime.datetime.now().strftime("%H:%M:%S")+'\nDevice Name :- '+request.user_agent.device.family+'\nOperating System :- '+request.user_agent.os.family+' '+request.user_agent.os.version_string+'\nBrowser :- '+request.user_agent.browser.family+' '+request.user_agent.browser.version_string+'\n\nHopefully it was you who logged in your Affiliator Affiliate Managemment Account.\n\nIf it was not you, please contact our Management Team to secure your account from fraud.\n\nThank You\nTeam Affiliator' 
            from_email = settings.EMAIL_HOST_USER
            to_list = [confirm_user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            return redirect("dashboard")
        
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
        
    else:
        return render(request, 'login.html')
    

def logout(request):
    auth.logout(request)
    
    return redirect('/')

def forgot_password(request):
    if request.method == "POST":
        if not request.POST['username']:
            messages.info(request, "Please enter your Registered username to continue!")
            return redirect("forgot_password")
        uname = request.POST['username']
        if uname:
            if User.objects.filter(username=uname).exists():
                
                if Password.objects.filter(username=uname).exists():
                    messages.info(request, "We have already sent the confirmation code to the email address associated with "+uname)
                    return redirect("enter_otp", uname)
                else:
                    curr_user = User.objects.get(username=uname)
                    digits = "0123456789"
                    otp = ""
                    for i in range(6):
                        otp += digits[math.floor(random.random()*10)]
                    new_otp = otp
                    print(new_otp)
                    pass_user = Password.objects.create(username=uname, otp=new_otp)
                    pass_user.save()
                    subject = 'Password Reset Request on Affiliator!'
                    message = 'Hi ' + curr_user.first_name + '!\n \nWe have recieved a password reset request on your User Account.\n\nYour Password reset code is ' + pass_user.otp +'\nIf it was not you, then please ignore.\n\nOur dedicated customer support team is always at your service.\nWishing you a happy online journey.\n\nThank You.\nTeam Affiliator'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [curr_user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)
                    messages.info(request, "Enter the OTP sent to registered email address asssociated with "+uname)
                    return redirect("enter_otp", uname)
            else:
                messages.info(request, "No user with Username " + uname)
                messages.info(request, "Please enter your registered Username")
                return redirect("forgot_password")
        else:
            messages.info(request, "Enter the username")
            return redirect("forgot_password")
    return render(request, "forgot_password.html")

def enter_otp(request, uname):
    if Password.objects.filter(username=uname).exists():
        pass_user = Password.objects.get(username=uname)
        curr_user = User.objects.get(username=uname)
        if request.method == "POST":
            if not request.POST['otp']:
                messages.info(request, "Please enter the OTP sent to your email address to continue!")
                return redirect("enter_otp", uname)
            curr_otp = request.POST['otp']
            if pass_user.otp == curr_otp:
                pass_user.confirmed = True
                pass_user.save()
                messages.info(request, "Email address confirmed")
                return redirect("new_password", uname)
            else:
                if pass_user.attempts < 4:
                    pass_user.attempts += 1
                    pass_user.save()
                    messages.info(request, "Incorrect otp, try again!" +str(5-pass_user.attempts)+" attempts left.")
                    return redirect("enter_otp", uname)
                else:
                    pass_user.attempts = 0
                    pass_user.save()
                    messages.info(request, "Maximum attempts held for this confirmation code. Sending another code to email associated with "+pass_user.username)
                    return redirect("resend_pass_code", uname)
        return render(request, "enter_otp.html", {'pass_user':pass_user})
    else:
        messages.info(request,"Enter the Registered username for which you want to change the Account Password.")
        return redirect("forgot_password")

def new_password(request, uname):
    if Password.objects.get(username=uname):
        pass_user = Password.objects.get(username=uname)
        curr_user = User.objects.get(username=uname)
        if request.method == "POST":
            if not request.POST['password1']:
                messages.info(request, "Please enter the Password to continue!")
                return redirect("enter_otp", uname)
            if not request.POST['password2']:
                messages.info(request, "Please enter the Password to continue!")
                return redirect("enter_otp", uname)
            if pass_user.confirmed:
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                if password1:
                    if password1 == password2:
                        password = make_password(password1, hasher='default')
                        curr_user.password = password
                        pass_user.delete()
                        curr_user.save()
                        messages.info(request, "Password changed successfully.")
                        return redirect("login")
                    else:
                        messages.info(request, "Passwords Don't Match. Please re-enter the Passwords.")
                        return redirect("new_password")
                else:
                    messages.info(request, "Password Fields cannot be blank.")
                    return redirect("new_password")
            else:
                messages.info(request, "Please enter your username registered with Affiliator")
                return redirect("forgot_password")
        return render(request, "new_password.html")
    else:
        messages.info(request, "Please enter your username registered with Affiliator")
        return redirect("forgot_password")

def resend_pass_code(request, uname):
    if Password.objects.filter(username=uname).exists():
        curr_user = User.objects.get(username=uname)
        pass_user = Password.objects.get(username=uname)
        digits = "0123456789"
        otp = ""
        for i in range(6):
            otp += digits[math.floor(random.random()*10)]
        new_otp = otp
        print(new_otp)
        pass_user.otp = new_otp
        pass_user.save()
        subject = 'Password Reset Request on Affiliator!'
        message = 'Hi ' + curr_user.first_name + '!\n \nWe have recieved a password reset request on your User Account.\n\nYour Password reset code is ' + pass_user.otp +'\nIf it was not you, then please ignore.\n\nOur dedicated customer support team is always at your service.\n Wishing you a happy online journey.\n\nThank You.\nTeam Affiliator'
        from_email = settings.EMAIL_HOST_USER
        to_list = [curr_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        messages.info(request, "Password reset code has been sent to email address associated with "+uname)
        return redirect("enter_otp", uname)
    else:
        messages.info(request, "Please enter the username first")
        return redirect("forgot_password")



def dashboard(request):
    if request.user.is_authenticated:
        user_info = Info.objects.get(username=request.user.username)
        if user_info.currency:

            ctr=0
            uo = Product.objects.filter(username = request.user.username)
            category = Product.objects.filter(username = request.user.username)
            new = Visitor_counter.objects.get(username = request.user.username)
            userpro = uo.all()
            li = list()
            user_info = Info.objects.get(username=request.user.username)
            if not category:
                bro = False
                
            
            for cat in category:
                if cat.product_category not in li:
                    li.append(cat.product_category)
                    bro = True
                    
                    
            for i in userpro:
                ctr+=1
            context = {
                "userpro":userpro,
                "ctr":ctr,
                "new":new,
                "category":category,
                "li":li,
                "bro":bro,
                "total_category":len(li),
                "user_info":user_info
            }
            return render(request, "index-dashboard.html", context)

        else:
            messages.info(request, "You haven't provided your website information yet. Please do so in order to access your Afiliator.in Dashboard.")
            return redirect("info")
    else:
        messages.info(request, "You need to login first in order to view your Affiliator Dashboard")
        return redirect("login")
        



def add_products(request):
    if request.user.is_authenticated:
        paid_user = Info.objects.get(username=request.user.username)
        if paid_user.currency:
            if request.method == "POST":
                
                username = request.user.username
                if not request.POST['product_image'] or not request.POST['product_name'] or not request.POST['product_text_link'] or not request.POST['product_description'] or not request.POST['product_price'] or not request.POST['product_category']:
                    messages.info(request, "Please enter all the fields!")
                    return redirect("add_products")
                product_image = request.POST['product_image']
                product_name = request.POST['product_name']
                product_text_link = request.POST['product_text_link']
                product_description = request.POST['product_description']
                product_price = request.POST['product_price']
                product_category = request.POST['product_category']
                
                
                pro = Product.objects.create(username=username,product_image=product_image,product_name=product_name,product_text_link=product_text_link,product_description=product_description,product_price=product_price,product_category=product_category)
                pro.save()
                messages.info(request, product_name + " added successfully!")
                
                
                
            
            uo = Product.objects.filter(username = request.user.username)
            userpro = uo.all()
            ca = Product.objects.filter(username = request.user.username)
            category = ca.all()
            if not category:
                bro = False
                    
            li = list()
            for cat in category:
                if cat.product_category not in li:
                    li.append(cat.product_category)
                    bro = True

            diction = {}
            ctr=0
            for list_item in li:
                for apj in category:
                    if apj.product_category == list_item:
                        ctr += 1
                diction[list_item] = ctr
                ctr=0

            
            context = {
                "userpro":userpro,
                "category":category,
                "li":li,
                "bro":bro,
                "diction":diction,
                "user_info":paid_user
            }
            
            return render(request, "add_products.html", context)
            
        else:
            messages.info(request, "You haven't provided your website information yet. Please do so in order to add products to your Afiliator.in Dashboard.")
            return redirect("info")  

    else:
        messages.info(request, "You need to login first in order to add products to your Affiliator Website")
        return redirect("login")

    
    
    
    
def delete(request, pro_id):
    if request.user.is_authenticated:
        edit_pro = get_object_or_404(Product,id=pro_id)
        inf = Info.objects.filter(username=request.user.username).first()
        if inf.website_name:
            if edit_pro.username == request.user.username:
                
                del_pro = Product.objects.get(id=pro_id)
                pro_name = del_pro.product_name
                del_pro.delete()
                messages.info(request, pro_name + " Deleted Successfully!")
                return redirect("dashboard")
            
            else:
                messages.info(request, "No such product to delete in your Affiliator website.")
                return redirect("dashboard")
        else:
            messages.info(request, "Please provide the information about your website.")
            return redirect("info")
    
    else:
        messages.info(request, "You need to login first in order to delete affiliate products from your Affiliator Website")
        return redirect("login")
    
    
def delete_pro(request, pro_id):
    if request.user.is_authenticated:
        edit_pro = get_object_or_404(Product,id=pro_id)
        inf = Info.objects.filter(username=request.user.username).first()
        if inf.website_name:
            if edit_pro.username == request.user.username:
                
                del_pro = Product.objects.get(id=pro_id)
                pro_name = del_pro.product_name
                del_pro.delete()
                messages.info(request, pro_name + " Deleted Successfully!")
                return redirect("add_products")
            
            else:
                messages.info(request, "No such product to delete in your Affiliator website.")
                return redirect("dashboard")
        else:
            messages.info(request, "Please provide the information about your website.")
            return redirect("info")
    
    else:
        messages.info(request, "You need to login first in order to delete products from your Affiliator website")
        return redirect("login")
    
    

def edit_product(request, pro_id):
    if request.user.is_authenticated:
        
        edit_pro = get_object_or_404(Product,id=pro_id)
        inf = Info.objects.filter(username=request.user.username).first()
        if inf.website_name:
            if edit_pro.username == request.user.username:
                
                if request.method == "POST":
                    if not request.POST['product_image'] or not request.POST['product_name'] or not request.POST['product_text_link'] or not request.POST['product_description'] or not request.POST['product_price'] or not request.POST['product_category']:
                        messages.info(request, "Please don't leave any field blank!")
                        return redirect("edit_product", pro_id)
                    username = request.user.username
                    product_image = request.POST['product_image']
                    product_name = request.POST['product_name']
                    product_text_link = request.POST['product_text_link']
                    product_description = request.POST['product_description']
                    product_price = request.POST['product_price']
                    product_category = request.POST['product_category']


                    edit = Product.objects.get(id=pro_id)
                    edit.product_image = product_image
                    edit.product_name = product_name
                    edit.product_text_link = product_text_link
                    edit.product_description = product_description
                    edit.product_price = product_price
                    edit.product_category
                    edit.save()
                    messages.info(request, product_name + " Changed Successfully.")





                edit = Product.objects.get(id=pro_id)
                uo = Product.objects.filter(username = request.user.username)
                userpro = uo.all()
                ca = Product.objects.filter(username = request.user.username)
                category = ca.all()
                li = list()
                if not category:
                    bro = False
                    
                for cat in category:
                    if cat.product_category not in li:
                        li.append(cat.product_category)
                        bro = True

                diction = {}
                ctr=0
                for list_item in li:
                    for apj in category:
                        if apj.product_category == list_item:
                            ctr += 1
                    diction[list_item] = ctr
                    ctr=0
            
                context = {
                    "userpro":userpro,
                    "edit":edit,
                    "category":category,
                    "li":li,
                    "bro":bro,
                    "diction":diction
                }

                return render(request, "edit_product.html", context)
            
            else:
                messages.info(request, "No such product to edit in your Affiliator website.")
                return redirect("dashboard")
        else:
            messages.info(request, "Please provide the information about your website.")
            return redirect("info")
            
    else:
        messages.info(request, "You need to login first in order to edit this product in your Affiliator Website")
        return redirect("login")


def edit(request):
    if request.user.is_authenticated:
        inf = Info.objects.filter(username=request.user.username).first()
        if inf.website_name:
            uo = Product.objects.filter(username = request.user.username)
            userpro = uo.all()
            ca = Product.objects.filter(username = request.user.username)
            category = ca.all()
            li = list()
            if not category:
                bro = False
                
            for cat in category:
                if cat.product_category not in li:
                    li.append(cat.product_category)
                    bro = True
        
            context = {
                "userpro":userpro,
                "category":category,
                "li":li,
                "bro":bro,
            }

            return render(request, "edit.html", context)
        else:
            messages.info(request, "Please provide the information about your website.")
            return redirect("info")
            
    else:
        messages.info(request, "You need to login first in order to edit this product in your Affiliator Website")
        return redirect("login")



    
def search(request):
    if request.user.is_authenticated:
        inf = Info.objects.filter(username=request.user.username).first()
        if inf.website_name:
            if request.method == "POST":
                query = request.POST["search"]
                search_object = Product.objects.filter(username = request.user.username).filter(product_name__icontains=query)
                
                ctr=0
                uo = Product.objects.filter(username = request.user.username)
                category = Product.objects.filter(username = request.user.username)
                new = Visitor_counter.objects.get(username = request.user.username)
                userpro = uo.all()
                li = list()
                if not category:
                    bro = False
                        
                    
                for cat in category:
                    if cat.product_category not in li:
                        li.append(cat.product_category)
                        bro = True
                            
                            
                for i in userpro:
                    ctr+=1

                context = {
                    "userpro":userpro,
                    "ctr":ctr,
                    "new":new,
                    "category":category,
                    "li":li,
                    "bro":bro,
                    "total_category":len(li),
                    "search":search_object,
                    "query":query,
                }
                return render(request, "index-dashboard.html", context)
            else:
                return redirect("dashboard")
        else:
            messages.info(request, "Please provide the information about your website.")
            return redirect("info")

    else:
        messages.info(request, "You need to login first in order to search affiliate products associated with your Affiliator Website")
        return redirect("login")
    

    
def info(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if not request.POST['currency']:
                messages.info(request, "Please enter the currency of the website!")
                return redirect("info")
            currency = request.POST["currency"]

            if not request.POST['website_name']:
                messages.info(request, "Please enter the Website Name!")
                return redirect("info")
            website_name = request.POST["website_name"]
            
            if not request.POST['website_title']:
                messages.info(request, "Please enter the Title of the website!")
                return redirect("info")
            website_title = request.POST["website_title"]
            
            if not request.POST['kind_of_products']:
                messages.info(request, "Please enter the kind of products you want to use!")
                return redirect("info")
            kind_of_products = request.POST["kind_of_products"]
            
            if not request.POST['country']:
                messages.info(request, "Please enter the Country or Region of the website!")
                return redirect("info")
            country = request.POST["country"]
            
            user_info = Info.objects.get(username=request.user.username)
            user_info.currency = currency
            user_info.website_name = website_name
            user_info.website_title = website_title
            user_info.kind_of_products = kind_of_products
            user_info.country = country
            
            user_info.save()

            return redirect("dashboard")
            
        else:
            infor = Info.objects.get(username=request.user.username)
            context = {
                "infor":infor
            }
            return render(request, "info.html", context)
    
    else:
        messages.info(request,"You need to login first in order to Add additional information for your Affiliator Website")
        return redirect("login")


def banner(request):
    if request.user.is_authenticated:
        inf = Info.objects.filter(username=request.user.username).first()
        if inf.website_name:
            if request.method == "POST":

                if request.POST.get("banner_link"):
                    banner_category = request.POST["banner_category"]
                    banner_link = request.POST["banner_link"]

                    banner_save = Banner.objects.create(username=request.user.username, banner_category=banner_category,banner_link=banner_link)
                    banner_save.save()
                    messages.info(request, "Banner Saved")
                    return redirect("banner")
                        
                elif request.POST.get("widget_link"):
                    widget_category = request.POST["widget_category"]
                    widget_link = request.POST["widget_link"]

                    widget_save = Widget.objects.create(username=request.user.username, widget_category=widget_category,widget_link=widget_link)
                    widget_save.save()
                    messages.info(request, "Widget Saved")
                    return redirect("banner")

                elif request.POST.get("tag"):
                    tag = request.POST["tag"]
                    if Tag.objects.filter(username=request.user.username).exists():
                        tag_save = Tag.objects.get(username=request.user.username)
                        tag_save.tag = tag
                        tag_save.save()
                        messages.info(request, "Tag Saved")
                        return redirect("banner")
                    
                    else:
                        tag_save = Tag.objects.create(username=request.user.username, tag=tag)
                        tag_save.save()
                        messages.info(request, "Tag Saved")
                        return redirect("banner")
                
                    

            category = Product.objects.filter(username = request.user.username)
            if not category:
                bro = False
                        
            li = list()
            for cat in category:
                if cat.product_category not in li:
                    li.append(cat.product_category)
                    bro = True

            diction = {}
            ctr=0
            for list_item in li:
                for apj in category:
                    if apj.product_category == list_item:
                        ctr += 1
                diction[list_item] = ctr
                ctr=0

            banner_obj = Banner.objects.filter(username=request.user.username)
            widget_obj = Widget.objects.filter(username=request.user.username)
            tag = Tag.objects.filter(username=request.user.username)
            for t in tag:
                tag = t

            context = {
                "bro":bro,
                "li":li,
                "category":category,
                "diction":diction,
                "ctr":ctr,
                "widget_obj":widget_obj,
                "banner_obj":banner_obj,
                'tag_obj':tag,

            }
            return render(request, "add_banner.html", context)
        else:
            messages.info(request, "Please provide the information about your website.")
            return redirect("info")

    else:
        messages.info(request, "Please Login First")
        return redirect("login")



def delete_banner(request, ban_id):
    if request.user.is_authenticated:
        inf = Info.objects.filter(username=request.user.username).first()
        if inf.website_name:
            edit_ban = get_object_or_404(Banner, id=ban_id)
            
            if edit_ban.username == request.user.username:
                
                del_ban = Banner.objects.get(id=ban_id)
                ban_name = del_ban.banner_category
                del_ban.delete()
                messages.info(request, ban_name + " associated Banner Deleted Successfully!")
                return redirect("banner")
            
            else:
                messages.info(request, "No such banner to delete in your Affiliator website.")
                return redirect("dashboard")
        else:
            messages.info(request, "Please provide the information about your website.")
            return redirect("info")
    
    else:
        messages.info(request, "You need to login first in order to delete products from your Affiliator website")
        return redirect("login")


def delete_widget(request, wid_id):
    if request.user.is_authenticated:
        inf = Info.objects.filter(username=request.user.username).first()
        if inf.website_name:
            edit_wid = get_object_or_404(Widget, id=wid_id)
            
            if edit_wid.username == request.user.username:
                
                del_wid = Widget.objects.get(id=wid_id)
                wid_name = del_wid.widget_category
                del_wid.delete()
                messages.info(request, wid_name + " associated Widget Deleted Successfully!")
                return redirect("banner")
            
            else:
                messages.info(request, "No such banner to delete in your Affiliator website.")
                return redirect("dashboard")
        else:
            messages.info(request, "Please provide the information about your website.")
            return redirect("info")
    
    else:
        messages.info(request, "You need to login first in order to delete products from your Affiliator website")
        return redirect("login")

