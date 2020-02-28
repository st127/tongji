from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .api.ajax import *
from django.contrib.auth.hashers import make_password, check_password
from pytz import timezone
import hashlib
from tongji.settings import get_upload_dir
import os


# Create your views here.


def index(request, class_id):
    # return HttpResponse("This is index")
    statistics = statistics_information.objects.filter(isDelete=False).filter(statistics_class=class_id)
    classes = class_information.objects.filter(isDelete=False).get(pk=class_id)
    names = classes.student_information_set.all()
    return render(request, 'xxtj/index.html', {
        'title': str(classes.name_dis) + '信息统计系统',
        'class_id': class_id,
        'class_name': str(classes.name_dis),
        'statistics': statistics,
        'names': names,
    })


def add(request):
    statistics = request.GET.get('statistics')
    name = request.GET.get('name')
    class_id = request.GET.get('class_id')
    statistics = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
    name = student_information.objects.filter(isDelete=False).get(pk=name)
    file_params = request.GET.get('file_params')
    if file_params:
        try:
            filelist = os.listdir(get_upload_dir() + file_params)
        except 	FileNotFoundError:
            return HttpResponse('文件时间戳已过期')
        else:
            pass
        return render(request, 'xxtj/add.html', {
            'statistics': statistics,
            'name': name,
            'class_id': class_id,
            'file_params': file_params,
            'file_list': filelist,
        })
    return render(request, 'xxtj/add.html', {
        'statistics': statistics,
        'name': name,
        'class_id': class_id,
        'file_params': file_params,
        # 'file_list': filelist,
    })


def ajax(request):
    do = request.GET.get('do')
    if do is None:
        return HttpResponse("Format Error!")
    if do == 'query_description_by_statistics':
        statistics = int(request.GET.get('statistics'))
        stu_id = request.GET.get('stu_id', default=0)
        if stu_id == '':
            stu_id = 0
        return query_description_by_statistics(statistics, stu_id)
    if do == 'add_recond':
        statistics = int(request.GET.get('statistics'))
        stu_id = int(request.GET.get('stu_id'))
        if request.GET.get('file_params'):
            return add_recond(statistics, stu_id, request.GET.get('file_params'))
        return add_recond(statistics, stu_id)
    if do == 'get_result_by_sta':
        statistics = int(request.GET.get('statistics'))
        ua = request.GET.get('ua', default='normal')
        return get_result_by_sta(statistics, ua)
    if do == 'clear_sta':
        statistics = int(request.GET.get('statistics'))
        return clear_sta(statistics)
    if do == 'add_description':
        json = request.GET.get('json')
        return add_description(json)
    if do == 'check_login_token':
        admin_id = request.GET.get('admin_id')
        token = request.GET.get('token')
        return check_login_token(token, admin_id)
    if do == 'print':
        return HttpResponse(request.GET.get('print'))



def result(request):
    admin_id = request.GET.get('admin_id')
    do = request.GET.get('do')
    if admin_id is None:
        return render(request, 'xxtj/result.html', {
            'title': "统计结果",
        })
    elif do is None:
        adm_sta = admin_information.objects.filter(isDelete=False).get(pk=int(admin_id))
        adm_sta = adm_sta.admin_statistics_set.filter(isDelete=False).all()
        statistics = {}
        for items in adm_sta:
            statistics[items.statistics.pk] = str(
                items.statistics.statistics_class.name_dis) + items.statistics.statistics_name
        # print(statistics)
        return render(request, 'xxtj/result.html', {
            'statistics': statistics,
            'title': "统计结果",
            'admin_id': admin_id,
        })
    elif do == "add_description":
        adm_sta = admin_information.objects.filter(isDelete=False).get(pk=int(admin_id))
        adm_sta = adm_sta.admin_statistics_set.filter(isDelete=False).all()
        statistics = {}

        for items in adm_sta:
            statistics[items.statistics.pk] = str(
                items.statistics.statistics_class.name_dis) + items.statistics.statistics_name
        return render(request, 'xxtj/admin/add_description.html', {
            'statistics': statistics,
            'title': "添加说明",
            'admin_id': admin_id,
            'save_id': hashlib.md5((str(d_tz.now()) + str(admin_id)).encode(encoding='UTF-8')).hexdigest(),
        })


def file(request):
    filenum_sum = request.POST.get("filenum_sum")
    upload_dir = get_upload_dir()
    try:
        os.mkdir(upload_dir + '/' + request.POST.get("save_id"))
    except FileExistsError:
        pass
    else:
        pass
    for file_num in range(0, int(filenum_sum)):
        f = request.FILES.get('file' + str(file_num))
        no_point_flag = True
        for foo in request.POST.get("fileName" + str(file_num)):
            if '.' == foo:
                no_point_flag = False
        if no_point_flag:
            file_name = upload_dir + request.POST.get("save_id") + '/' + request.POST.get("fileName" + str(file_num)).replace('%3A','') + ".jpg"
        else:
            file_name = upload_dir + request.POST.get("save_id") + '/' + request.POST.get("fileName" + str(file_num))
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    stat = {
        'status': "success",
    }
    return JsonResponse(stat)
