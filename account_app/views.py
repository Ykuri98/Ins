from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import HttpResponse
from account_app import models
import os
import time
import re
from PIL import Image
import uuid
import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password ,check_password
from django.conf import settings
from datetime import datetime
from PIL import Image
import filetype

def register(request):
    error_msg = ""
    if(request.method)=="POST":
        email= request.POST.get("email",None)
        username = request.POST.get("username",None)
        password = request.POST.get("password", None)
        passwordRepeat = request.POST.get("passwordRepeat", None)

        if (models.Login.objects.filter(EmailAddress=email)):
            error_msg = "email already taken"
        elif(models.Login.objects.filter(username=username)):
            error_msg = "username already taken"
        else:
            user=models.Login.objects.create(username=username, password=password,EmailAddress=email)
            user.password = make_password(user.password)
            user.save()
            user = auth.authenticate(EmailAddress=email, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                request.session['email'] = email
                return HttpResponseRedirect('/main')
    return render(request, "registration.html", {'error_msg': error_msg})


def main(request):
    if (loginRedirect(request) is True):
        return  render(request, "main.html")
    else:
        return HttpResponseRedirect(reverse('landing'))

def login(request):
    if (loginRedirect(request) is True):
        return HttpResponseRedirect('/main');
    error_msg = ""
    if (request.method)=='POST':
        item = request.POST.get("email", None)
        password = request.POST.get("password", None)

        if ('@' in item):
            user = auth.authenticate(EmailAddress=item, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                request.session['email'] = item
                return HttpResponseRedirect('/main')
            else:
                try:
                    models.Login.objects.get(EmailAddress=item)
                    error_msg = "password is invalid."
                except:
                    error_msg = "email not found."
        else:
            user = auth.authenticate(EmailAddress=models.Login.objects.get(username=item).EmailAddress, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                request.session['email'] = models.Login.objects.get(username=item).EmailAddress
                return HttpResponseRedirect('/main')
            else:
                try:
                    models.Login.objects.get(username=item)
                    error_msg = "password is invalid."
                except:
                    error_msg = "email not found."
    return render(request,"login.html",{'error_msg':error_msg})


@login_required
def me(request):
    email = request.session.get('email')
    print(email)
    user_list = models.Login.objects.get(EmailAddress=email)
    username = user_list.username
    password = user_list.password
    return render(request, "user+information.html",{'username':username,'email':email})

def loginRedirect(request):
    if request.user.is_authenticated:
        return  True
        # return HttpResponseRedirect(reverse('profile'))
    else:
        return HttpResponseRedirect(reverse('landing'))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))

def landing(request):
    return render(request, "landing page.html")

@login_required
def profile(request):
    error_msg = ""
    email = request.session.get('email')
    user_list = models.Login.objects.get(EmailAddress=email)
    username = user_list.username
    password = user_list.password
    if (request.method) == 'POST':
        newemail = request.POST.get("email", None)
        oldpassword = request.POST.get("oldpassword", None)
        newpassword1 = request.POST.get("newpassword1", None)
        newpassword2 = request.POST.get("newpassword2", None)
        if newemail == '':
            if check_password(oldpassword, password):
                user = models.Login.objects.get(EmailAddress=email)
                user.password = newpassword1
                user.password = make_password(user.password)
                user.save()
                request.session['email'] = email
            else:
                error_msg = "invalid password."
        elif oldpassword == '':
            try:
                userinfo = models.Login.objects.get(EmailAddress=newemail)
            except:
                userinfo = None

            if userinfo:
                error_msg = "email already taken."
            else:
                auth.logout(request)
                user = models.Login.objects.get(EmailAddress=email)
                user.EmailAddress = newemail
                user.save()
                userinfo = auth.authenticate(EmailAddress=newemail, password=password)
                print(userinfo)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    request.session['email'] = newemail
                    return HttpResponseRedirect('/main')
        elif newemail != '' and oldpassword != '':
            if check_password(oldpassword,password):
                try:
                    userinfo = models.Login.objects.get(EmailAddress=newemail)
                except:
                    userinfo = None

                if userinfo:
                    error_msg = "email already taken."
                else:
                    user = models.Login.objects.get(EmailAddress=email)
                    user.EmailAddress = newemail
                    user.password = newpassword1
                    user.password = make_password(user.password)
                    user.save()
                    request.session['email'] = newemail
            else:
                error_msg = "invalid password."
    return render(request, "profile page.html",{'error_msg':error_msg,'username':username})

def upload(request):
    fi = request.FILES['pic']
    email = request.session.get('email')
    txt = request.POST["txt"]
    user_list = models.Login.objects.get(EmailAddress=email)
    username = user_list.username
    fname = os.path.join(settings.MEDIA_ROOT, username)
    if not os.path.exists(fname):
        os.makedirs(fname)
    ##使用PIL库对图片操作
    fname = PIL(fi,fname)

    p = models.Picture.objects.create_pic(fname,txt,datetime.now())
    info = models.Picture.objects.get(path=fname)
    info1 = models.Picture.objects.filter().order_by('-createTime')

    list = []
    for i in info1:
        imgpath = i.path.split(os.path.sep)
        imgpath.reverse()
        uploadtime = i.createTime.strftime('%Y-%m-%d %H:%M')
        like = i.like
        path = imgpath[2] + "/" + imgpath[1] + "/" + imgpath[0]
        name = imgpath[1]
        item = {}
        item['uploadtime'] = uploadtime
        item['like'] = like
        item['path'] = path
        item['name'] = name
        list.append(item)
    return render(request, "main.html",{'info1':list})

def main(request):
    info1 = models.Picture.objects.filter().order_by('-createTime')
    list = []
    for i in info1:
        imgpath = i.path.split(os.path.sep)
        imgpath.reverse()
        uploadtime = i.createTime.strftime('%Y-%m-%d %H:%M')
        like = i.like
        path = imgpath[2] + "/" + imgpath[1] + "/" + imgpath[0]
        name = imgpath[1]
        item = {}
        item['uploadtime'] = uploadtime
        item['like'] = like
        item['path'] = path
        item['name'] = name
        list.append(item)
    return render(request, "main.html",{'info1':list})

def PIL(fi,fname):
    img = Image.open(fi)
    name = str(uuid.uuid1())
    ##判断图片是否为jpg，大小是否超过1000*1000
    if img.format == 'JPG'and img.size < (1000,1000):
        ##对fname读取并在目标文件生成图片
        fname = os.path.join(fname, name+",jpg")
        with open(fname, 'wb') as pic:
            for c in fi.chunks():
                pic.write(c)
    else:
        if img.size < (1000,1000):
            ##问题：不能保存JPG格式
            fname = os.path.join(fname, name+".jpg")
            img = img.convert('RGB')
            img.save(fname, 'jpeg')
        else :
            (x,y) = img.size
            if(1.0*x/1000) > (1.0*y/1000):
                scale = 1.0 * x /1000
                img = img.resize((int(x / scale), int(y / scale)),Image.ANTIALIAS)
            else:
                scale = 1.0 * y / 1000
                img = img.resize((int(x / scale), int(y / scale)), Image.ANTIALIAS)
            fname = os.path.join(fname, name+".jpg")
            img = img.convert('RGB')
            img.save(fname, 'jpeg')
    return fname

def checkfile(request):
    allow = ['jpg','png','gif']
    fi = request.FILES['file']
    email = request.session.get('email')
    user_list = models.Login.objects.get(EmailAddress=email)
    username = user_list.username
    fname = os.path.join(settings.MEDIA_ROOT, username)
    if not os.path.exists(fname):
        os.makedirs(fname)
    fname = os.path.join(fname, fi.name)
    with open(fname, 'wb') as pic:
        for c in fi.chunks():
            pic.write(c)
    kind = filetype.guess(fname)
    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)
    os.remove(fname)
    if kind.extension in allow:
        return HttpResponse(1)
    return HttpResponse(0)


#   思考：用JS判断文件类型，
#   文件类型不符，则提示错误信息
#   只有文件类型符合时，才能提交请求。
# 类似：
#     function checkImgType(ths){    验证文件类型，  仅返回值为True时才能提交
#         if (ths.value == "") {
#             alert("请上传图片");
#             return false;
#         } else {
#             if (!/\.(gif|jpg|jpeg|png|GIF|JPG|PNG)$/.test(ths.value)) {
#                 alert("图片类型必须是.gif,jpeg,jpg,png中的一种");
#                 ths.value = "";
#                 return false;
#             }
#         }
#         return true;
#     }