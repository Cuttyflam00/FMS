from django.shortcuts import render
from django.http import HttpResponse

def email(request):
     return render(request, 'email.html')