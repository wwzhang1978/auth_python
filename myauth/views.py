from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import 自定义注册表单, 自定义编辑表单, 登录表单
from .models import 普通会员表
from django.contrib.auth.decorators import login_required
# Create your views here.

def 主页(request):

    return render(request, 'myauth/home.html')

def 登录(request):
    if request.method == 'POST':
        login_form = 登录表单(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            login(request, user)
            return redirect('myauth:主页')
    else:
        login_form = 登录表单()
    context = {
        'login_form': login_form,
        'user': request.user,
    }
    return render(request, 'myauth/login.html', context)

def 登出(request):
    logout(request)
    return redirect('myauth:主页')

def 注册(request):
    if request.method == 'POST':
        # reg_form = UserCreationForm(request.POST) Django基础版本
        reg_form = 自定义注册表单(request.POST)  #通过forms.py自定义表单
        if reg_form.is_valid():
            reg_form.save()
            user = authenticate(username=reg_form.cleaned_data['username'],password=reg_form.cleaned_data['password1'])
            user.email=reg_form.cleaned_data['email']
            普通会员表(用户=user,昵称=reg_form.cleaned_data['昵称'],生日=reg_form.cleaned_data['生日']).save()
            login(request,user)
            return redirect("myauth:主页")
    else:
        reg_form = 自定义注册表单()
    context = {
        'regform': reg_form,
    }
    return render(request,'myauth/register.html',context)

@login_required(login_url='myauth:登录')
def 个人中心(request):
    context={
        'user': request.user,
    }
    return render(request,'myauth/user_center.html',context)

@login_required(login_url='myauth:登录')
def 编辑信息(request):
    if request.method == 'POST':
        # reg_form = UserCreationForm(request.POST) Django基础版本
        edit_form = 自定义编辑表单(request.POST,instance=request.user)  #通过forms.py自定义表单
        if edit_form.is_valid():
            edit_form.save()
            # 普通会员表(用户=user,昵称=reg_form.cleaned_data['昵称'],生日=reg_form.cleaned_data['生日']).save()
            # login(request,user)
            request.user.普通会员表.昵称 = edit_form.cleaned_data['昵称']
            request.user.普通会员表.生日 = edit_form.cleaned_data['生日']
            request.user.普通会员表.save()
            return redirect("myauth:个人中心")
    else:
        edit_form = 自定义编辑表单(instance=request.user)

    context = {
        'edit_form': edit_form,
        'user':request.user,
    }
    return render(request,'myauth/edit_profile.html',context)

@login_required(login_url='myauth:登录')
def 修改密码(request):
    if request.method == 'POST':
        # reg_form = UserCreationForm(request.POST) Django基础版本
        pwd_form = PasswordChangeForm(data=request.POST, user=request.user)  #通过forms.py自定义表单
        if pwd_form.is_valid():
            pwd_form.save()
            # 普通会员表(用户=user,昵称=reg_form.cleaned_data['昵称'],生日=reg_form.cleaned_data['生日']).save()
            # login(request,user)
            return redirect("myauth:登录")
    else:
        pwd_form = PasswordChangeForm(user=request.user)

    context = {
        'edit_form': pwd_form,
        'user':request.user,
    }
    return render(request,'myauth/pwd_change.html',context)