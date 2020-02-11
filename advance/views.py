from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone as d_tz
import hashlib
from .api.ajax import *


# Create your views here.


def login(request):
    admin_id = request.GET.get('admin_id')
    do = request.POST.get('do')
    if do == "verify":
        username = request.POST.get('username')
        password = request.POST.get('password')
        token = request.POST.get('token')
        admin_info = admin_information.objects.filter(isDelete=False).get(admin_username=username)
        if check_password(password, admin_info.admin_password):
            m = hashlib.md5()
            md5_str = "token_tongji_" + str(admin_info.admin_username) + str(d_tz.now())
            md5_str = md5_str.encode(encoding='utf-8')
            m.update(md5_str)
            md5_str = m.hexdigest()
            admin_info.token = md5_str
            admin_info.save()
            response = redirect('advance:index')
            response.set_cookie('token', value=md5_str, max_age=365 * 24 * 60 * 60)
            response.set_cookie('admin_id', value=admin_info.pk, max_age=365 * 24 * 60 * 60)
            return response
    if request.COOKIES.get('token') and request.COOKIES.get('admin_id'):
        sta_inf = admin_information.objects.filter(isDelete=False).get(pk=request.COOKIES.get('admin_id'))
        if request.COOKIES.get('token') == sta_inf.token:
            return redirect('advance:index')
    if admin_id is None:
        username = ''
    else:
        username = admin_information.objects.filter(isDelete=False).get(pk=admin_id).admin_username
    return render(request, 'advance/login.html', {
        "username": username,
    })


def index(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    admin_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
    if admin_inf.token == token:
        return render(request, 'advance/index.html', {

        })
    else:
        return redirect('xxtj:login')


def cla_inf(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    stu_id = request.GET.get('stu')
    cla_id = request.GET.get('cla')
    if stu_id:
        stu_inf = student_information.objects.filter(isDelete=False).get(pk=stu_id)
        class_inf = [stu_inf.student_class]
        # print(class_inf)
        return render(request, 'advance/class/inf.html', {
            'cla_inf': class_inf,
        })
    if cla_id:
        class_inf = class_information.objects.filter(isDelete=False).get(pk=cla_id)
        return render(request, 'advance/class/inf.html', {
            'cla_inf': [class_inf],
        })
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        class_inf = class_information.objects.filter(isDelete=False).all()
        return render(request, 'advance/class/inf.html', {
            'cla_inf': class_inf,
        })
    else:
        return redirect('advance:login')


def add_cla(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        # class_inf = class_information.objects.filter(isDelete=False).all()
        return render(request, 'advance/class/add.html')
    else:
        return redirect('advance:login')


def del_cla(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    class_id = request.GET.get('class')
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        class_inf = class_information.objects.filter(isDelete=False).get(pk=class_id)
        stu_inf = class_inf.student_information_set.filter(isDelete=False).all()
        sta_inf = class_inf.statistics_information_set.filter(isDelete=False).all()
        return render(request, 'advance/class/del.html', {
            'class': class_inf,
            'stu_inf': stu_inf,
            'sta_inf': sta_inf,
        })
    else:
        return redirect('advance:login')


def edit_cla(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    class_id = request.GET.get('class')
    if not class_id:
        class_inf = class_information.objects.filter(isDelete=False).all()
        return render(request, 'advance/class/inf.html', {
            'cla_inf': class_inf,
            'inf': "请选择班级以修改",
        })
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        class_inf = class_information.objects.filter(isDelete=False).get(pk=class_id)
        return render(request, 'advance/class/edit.html', {
            'cla_inf': class_inf,
        })
    else:
        return redirect('advance:login')


def stu_inf(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    cla_id = request.GET.get('class')
    if cla_id:
        cla_inf = class_information.objects.filter(isDelete=False).get(pk=cla_id)
        stu_inf = cla_inf.student_information_set.filter(isDelete=False).all()
        return render(request, 'advance/student/inf.html', {
            'stu_inf': stu_inf,
            'inf': "以下是" + cla_inf.name_dis + "的学生",
        })
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        stu_inf = student_information.objects.filter(isDelete=False).all()
        return render(request, 'advance/student/inf.html', {
            'stu_inf': stu_inf,
        })
    else:
        return redirect('advance:login')


def add_stu(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        class_inf = class_information.objects.filter(isDelete=False).all()
        return render(request, 'advance/student/add.html', {
            'class_inf': class_inf,
        })
    else:
        return redirect('advance:login')


def del_stu(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    stu_id = request.GET.get('stu')
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        stu_inf = student_information.objects.filter(isDelete=False).get(pk=stu_id)
        rec_inf = stu_inf.recond_set.filter(isDelete=False).all()
        return render(request, 'advance/student/del.html', {
            'stu_inf': stu_inf,
            'rec_inf': rec_inf,
        })
    else:
        return redirect('advance:login')


def edit_stu(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    stu_id = request.GET.get('stu')
    if not stu_id:
        stu_inf = student_information.objects.filter(isDelete=False).all()
        return render(request, 'advance/student/inf.html', {
            'stu_inf': stu_inf,
            'inf': "请选择学生以编辑",
        })
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        stu_inf = student_information.objects.filter(isDelete=False).get(pk=stu_id)
        class_inf = class_information.objects.filter(isDelete=False).all()
        stu_cla = stu_inf.student_class.pk
        return render(request, 'advance/student/edit.html', {
            'stu_inf': stu_inf,
            'class_inf': class_inf,
            'stu_cla': stu_cla,
        })
    else:
        return redirect('advance:login')


def sta_inf(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    cla_id = request.GET.get('class')
    if cla_id:
        cla_inf = class_information.objects.filter(isDelete=False).get(pk=cla_id)
        sta_inf = cla_inf.statistics_information_set.filter(isDelete=False).all()
        return render(request, 'advance/statistics/inf.html', {
            'sta_inf': sta_inf,
            'inf': "以下是" + cla_inf.name_dis + "的统计",
        })
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        sta_inf = statistics_information.objects.filter(isDelete=False).all()
        return render(request, 'advance/statistics/inf.html', {
            'sta_inf': sta_inf,
        })
    else:
        return redirect('advance:login')


def add_sta(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        class_inf = class_information.objects.filter(isDelete=False).all()
        return render(request, 'advance/statistics/add.html', {
            'class_inf': class_inf,
        })
    else:
        return redirect('advance:login')


def del_sta(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    sta_id = request.GET.get('sta')
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=sta_id)
        rec_inf = sta_inf.recond_set.filter(isDelete=False).all()
        return render(request, 'advance/statistics/del.html', {
            'sta_inf': sta_inf,
            'rec_inf': rec_inf,
        })
    else:
        return redirect('advance:login')


def edit_sta(request):
    admin_id = request.COOKIES.get('admin_id')
    token = request.COOKIES.get('token')
    sta_id = request.GET.get('sta')
    if not sta_id:
        sta_inf = statistics_information.objects.filter(isDelete=False).all()
        return render(request, 'advance/statistics/inf.html', {
            'sta_inf': sta_inf,
            'inf': "请选择统计以编辑",
        })
    if admin_id:
        adm_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        if adm_inf.token != token:
            return redirect('advance:login')
        sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=sta_id)
        class_inf = class_information.objects.filter(isDelete=False).all()
        sta_cla = sta_inf.statistics_class.pk
        return render(request, 'advance/statistics/edit.html', {
            'sta_inf': sta_inf,
            'class_inf': class_inf,
            'sta_cla': sta_cla,
        })
    else:
        return redirect('advance:login')


def ajax(request):
    do = request.GET.get('do')
    if do == 'add_cla':
        return add_cla_ajax(request)
    if do == 'edit_cla':
        return edit_cla_ajax(request)
    if do == 'del_cla':
        return del_class_ajax(request)
    if do == 'add_stu':
        return add_stu_ajax(request)
    if do == 'del_stu':
        return del_stu_ajax(request)
    if do == 'edit_stu':
        return edit_stu_ajax(request)
    if do == 'add_sta':
        return add_sta_ajax(request)
    if do == 'del_sta':
        return del_sta_ajax(request)
    if do == 'edit_sta':
        return edit_sta_ajax(request)
