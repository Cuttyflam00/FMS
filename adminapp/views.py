from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from fms_django.settings import MEDIA_ROOT, MEDIA_URL
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from fmsApp.models import Post
from cryptography.fernet import Fernet
from django.conf import settings

context = {
    'page_title' : 'File Management System',
}

def admin(request):
    context['page_title'] = 'User Lists'
    request.user.is_superuser
    users = User.objects.all()
    context['users'] = users
    context['usersLen'] = users.count()
    print(request.build_absolute_uri())
    return render(request, 'userlist.html',context)


@login_required
def delete_user(request):
    resp = {'status':'failed', 'msg':''}
    if request.method == 'POST':
        try:
            user = User.objects.get(id = request.POST['id'])
            user.delete()
            resp['status'] = 'success'
            messages.success(request, 'User has been deleted successfully')
        except:
           resp['msg'] = "Undefined User ID"
    return HttpResponse(json.dumps(resp),content_type="application/json")