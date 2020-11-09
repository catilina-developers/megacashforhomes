from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from .models import *
import requests as rq
import json
from datetime import datetime, timedelta
import math
import time
from num2words import num2words as nw

# Create your views here.

def robot_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: ",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_not_address(user_mail, admin_email, sender, cust_name, cust_phone, location, price):
    cust_msg = "our team will contact you sortly!"
    admin_msg ="""
    Customer Name: %s
    Property Location: %s
    Phone no: %s
    Email: %s
    Expected Price: %s
    unable to get the address of this property.
    """%(str(cust_name), str(location), str(cust_phone), str(user_mail), str(price))
    send_mail(
        "Oops Address might not be valild",
        cust_msg,
        sender,
        [user_mail]
    )
    admin_email = admin_email.split(",")
    send_mail(
        "Address not found",
        admin_msg,
        sender,
        admin_email
    )
def send_not_zestimate(user_mail, admin_email, sender, cust_name, cust_phone, location, price):
    cust_msg = "our team will contact you sortly!"
    admin_msg ="""
    Customer Name: %s
    Property Location: %s
    Phone no: %s
    Email: %s
    Expected Price: %s
    unable to get the zestimate of this property.
    """%(str(cust_name), str(location), str(cust_phone), str(user_mail), str(price))
    send_mail(
        "Oops Address might not be valild",
        cust_msg,
        sender,
        [user_mail]
    )
    admin_email = admin_email.split(",")
    send_mail(
        "zestimate not found",
        admin_msg,
        sender,
        admin_email
    )
def send_on_success(user_mail, admin_email, sender, cust_name, cust_phone, location, price, result):
    mail_subj = "Congratulation for join with us" #success mail subject
    user_msg = "<div style='font-size:16px;font-color:black'>Dear <strong>%s</strong> <br/>We are glad to purchase your property. Please follow the bellow pdf guideline.<br/>Thank you<br/><strong>Best regards</strong><br/><strong>Mega Cash for homes</strong></div>"%(cust_name)
    admin_msg ="""
    Customer Name: %s
    Property Location: %s
    Phone no: %s
    Email: %s
    Expected Price: %s
    you get a new Agreement.
    """%(str(cust_name), str(location), str(cust_phone), str(user_mail), str(price))
    email = EmailMessage(
        mail_subj,
        user_msg,
        sender,
        [user_mail],
        reply_to=['no-reply@gmail.com'],
    )
    email.content_subtype="html"
    email.attach("Agreement.pdf", result.getvalue(), "application/pdf")
    email.send()
    admin_email = admin_email.split(",")
    email = EmailMessage(
        "New User Agreement",
        admin_msg,
        sender,
        admin_email,
        reply_to=['no-reply@gmail.com'],
    )
    email.attach("Agreement.pdf", result.getvalue(), "application/pdf")
    email.send()


def pdf(request):
    if request.method == 'POST':
        price = request.POST['price']
        condition = request.POST['condition']
        curr_day = date.today()
        today = curr_day.strftime("%B %d, %Y")
        last_date = curr_day + timedelta(90)
        last_date = last_date.strftime("%B %d, %Y")
        template_path = 'acc/agreement.html'
        location = request.POST['location']
        cust_name = request.POST['cust_name']
        cust_email = request.POST['cust_email']
        img_path = "http://127.0.0.1:8000/static/images/loc.jpg"
        cust_phone = request.POST['phone']
        admin_email = "agentnate@gmail.com, dsifers@gmail.com" 
        sender = "Megacashforhomes@gmail.com" 
        

        #address validation goes here
        url = "https://realtor.p.rapidapi.com/locations/auto-complete"

        querystring = {"input":location}

        headers = {
            'x-rapidapi-host': "realtor.p.rapidapi.com",
            'x-rapidapi-key': "b7a378bf63msh0c87c5ffcb7c2ddp122fa1jsn242709ad6afc" #"4c93f0d8ecmshd6f225dfbcc7675p1d95cfjsn33f2a1d1b952"
            }
        addr = ''
        citystatezip = ''
        #end address validation
        try:
            add_res = rq.request("GET", url, headers=headers, params=querystring)
            address = json.loads(add_res.text)
            addr = address["autocomplete"][0]["mpr_id"]
        except:
            send_not_address(cust_email, admin_email, sender, cust_name, cust_phone, location, price)
            return render(request, "acc/sell.html", {"address_not_found":True})
        url = "https://realtor.p.rapidapi.com/properties/v2/detail"
        querystring = {"property_id":addr}
        zestimate = None
        price_spell = None
        try:
            response = rq.request("GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)
            data = data["properties"][0]
            zestimate = "{:,}".format(math.ceil(int(data["price"])*.6))
            price_spell = nw(math.ceil(int(data["price"])*.6))
            zestimate = "$"+str(zestimate)
        except:
            send_not_zestimate(cust_email, admin_email, sender, cust_name, cust_phone, location, price)
            return render(request, "acc/sell.html", {"address_not_found":True})
        #end code
        cust = Customer(name=cust_name, price=price, location=location, mail=cust_email, condition=condition)
        cust.save()
        context = {"location": location,
                   "cust_name": cust_name,
                   "cust_email": cust_email,
                   "price": zestimate,
                   "price_spell": price_spell,
                   "date": today,
                   "zestimate":zestimate,
                   "last_date":last_date,
                   "phone":cust_phone
                   }
        template = get_template(template_path)
        html = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if pdf.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        else:
            res_data = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = "Agreement.pdf"
            content = "inline; filename=%s"%(filename)
            res_data["Content-Disposition"] = content
            send_on_success(cust_email, admin_email, sender, cust_name, cust_phone, location, price, result)
            return res_data

        return render(request, 'acc/index.html')


    else:
        return render(request, 'acc/index.html')
    #to database




t1 = Testimonial.objects.get(id=1)
t2 = Testimonial.objects.get(id=2)
t3 = Testimonial.objects.get(id=3)
t4 = Testimonial.objects.get(id=4)
t5 = Testimonial.objects.get(id=5)
context = {'t1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5}


def home(request):
    ip = visitor_ip_address(request)
    if len(Users_ip.objects.filter(user_ip=ip)) == 0:
        user = Users_ip(user_ip=ip)
        user.save()
    return render(request, 'acc/index.html', context)


def about(request):
    ip = visitor_ip_address(request)
    if len(Users_ip.objects.filter(user_ip=ip)) == 0:
        user = Users_ip(user_ip=ip)
        user.save()
    return render(request, 'acc/about.html', context)


def blog(request):
    ip = visitor_ip_address(request)
    if len(Users_ip.objects.filter(user_ip=ip)) == 0:
        user = Users_ip(user_ip=ip)
        user.save()
    bg1 = Blog.objects.get(id=1)
    bg2 = Blog.objects.get(id=2)
    bg3 = Blog.objects.get(id=3)
    bg4 = Blog.objects.get(id=4)
    bg5 = Blog.objects.get(id=5)
    bg6 = Blog.objects.get(id=6)
    context = {'bg1': bg1, 'bg2': bg2, 'bg3': bg3, 'bg4': bg4, 'bg5': bg5, 'bg6': bg6}
    return render(request, 'acc/blog.html', context)


def contact(request):
    ip = visitor_ip_address(request)
    if len(Users_ip.objects.filter(user_ip=ip)) == 0:
        user = Users_ip(user_ip=ip)
        user.save()
    if request.method == 'POST':
        name = request.POST["cust_name"]
        email = request.POST['cust_mail']
        subject = request.POST["subject"]
        message = request.POST["message"]
        admin_email = "agentnate@gmail.com, dsifers@gmail.com" 
        mail_msg = "You have a query by :"+name+"\nEmail id: "+email+"\nSubject: "+subject+"\nPerson wants to ask following: \n"+message+""
        sender = "Megacashforhomes@gmail.com"
        admin_email = admin_email.split(',')
        send_mail(
            "You have a query",
            mail_msg,
            sender,
            admin_email
        )
        return render(request, 'acc/index.html')
    else:
        return render(request, 'acc/contact.html')


def meet(request):
    ip = visitor_ip_address(request)
    if len(Users_ip.objects.filter(user_ip=ip)) == 0:
        user = Users_ip(user_ip=ip)
        user.save()
    if request.method == 'POST':
        phone = request.POST['phone']
        name = request.POST["cust_name"]
        email = request.POST['cust_email']
        location = request.POST['property_addr']
        message = "Meeting request is Made by " + name + "\nCustomer email address is : " + email + "\nseller's property location:" + location + "\nCustomers Phone number: "+ phone +""
        admin_email = "agentnate@gmail.com, dsifers@gmail.com"
        sender = "Megacashforhomes@gmail.com"
        admin_email = admin_email.split(',')
        print(sender)
        send_mail(
            "You have a meet request",
            message,
            sender,
            admin_email
        )
        cust_msg = "we got you request for the meeting. We will connect back to you for further details"
        send_mail(
            "Thank you for join with us!",
            cust_msg,
            sender,
            [email]
        )
        # time.sleep(100)
        print("mail sent")
        return render(request, 'acc/index.html')
    else:
        return render(request, 'acc/meet.html')


def sell(request):
    ip = visitor_ip_address(request)
    if len(Users_ip.objects.filter(user_ip=ip)) == 0:
        user = Users_ip(user_ip=ip)
        user.save()
    return render(request, 'acc/sell.html')


def blogs(request, pk_test):
    ip = visitor_ip_address(request)
    if len(Users_ip.objects.filter(user_ip=ip)) == 0:
        user = Users_ip(user_ip=ip)
        user.save()
    blogs = Blog.objects.get(id=pk_test)
    context = {'blog': blogs}
    return render(request, 'acc/blogs.html', context)
