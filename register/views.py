from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from register.models import User
import random
import string
from register.captcha.image import ImageCaptcha


# Create your views here.
def login(request):
    username = request.COOKIES.get('username')
    password = request.COOKIES.get('password')
    user = User.objects.filter(username=username, password=password)
    if user:
        request.session['is_login'] = True
        return redirect('/page/index/')
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def select(request):
    return render(request, 'sel.html')


def get_captcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_letters + string.digits, 4)
    code = "".join(code)
    print(code)
    data = image.generate(code)
    request.session['code'] = code
    return HttpResponse(data, "image/png")


def index(request):
    is_login = request.session.get('is_login')
    if is_login:
        users = User.objects.all()
        return render(request, 'index.html', {'users': users})
    return render(request, 'login.html')


def receive_login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    remember = request.POST.get('remember')
    captcha = request.POST.get("captcha")
    code = request.session.get("code")
    if captcha.lower() != code.lower():
        return HttpResponse("验证码不正确")
    count = User.objects.filter(username=username, password=password)
    if count:
        request.session['is_login'] = True
        res = redirect(to='/page/index/')
        if remember:
            res.set_cookie('username', username, max_age=3600 * 24 * 7)
            res.set_cookie('password', password, max_age=3600 * 24 * 7)
        return res
    return redirect(to='/page/login/')


def receive_register(request):
    try:
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        with transaction.atomic():
            user = User.objects.create(username=username, password=password)
            if user:
                return redirect(to='/page/login/')
    except:
        return HttpResponse('注册失败')
