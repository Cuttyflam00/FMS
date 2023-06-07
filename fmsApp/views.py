from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from fms_django.settings import MEDIA_ROOT, MEDIA_URL
import json
import pyotp
import qrcode
import io
import time
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from fmsApp.forms import UserRegistration, SavePost, UpdateProfile, UpdatePasswords
from fmsApp.models import Post
from cryptography.fernet import Fernet
from django.conf import settings
import base64
# Create your views here.

context = {
    'page_title' : 'File Management System',
}
#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    otp = ''
    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        otp = request.POST['otp']
        secret_key = username + 'FMSAPP'
        print(otp)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if username == 'admin':
                    login(request, user)
                else: 
                    print(otp)
                    print(secret_key)   
                    totp = pyotp.TOTP(secret_key)
                    if totp.verify(otp):
                        login(request, user)
                        resp['status']='success'
                    else:
                        resp['msg'] = "Incorrect OTP"
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    context['page_title'] = 'Home'
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(user = request.user).all()
    context['posts'] = posts
    context['postsLen'] = posts.count()
    print(request.build_absolute_uri())
    return render(request, 'home.html',context)

def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        data = request.POST

        form = UserRegistration(data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username=username, password=pwd)
            login(request, loginUser)
            return redirect('scanQRcode')
        else:
            context['reg_form'] = form

    return render(request, 'register.html', context)


def scanQRcode(request):
    return render(request,'scanQRcode.html',context)

def genQRcode(request):
    secret_key = request.user.username + 'FMSAPP'
    print(secret_key)
    # Generate the QR code
    otp_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=request.user.username, issuer_name='FMSApp')
     # Save the image to an in-memory buffer
    qr = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, "qrcode.png")
    buffer.seek(0)

    # Create an HTTP response with the image content type
    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = 'inline; filename="qrcode.png"'

    # Set the content of the response to the image buffer
    response.write(buffer.getvalue())
    return response
