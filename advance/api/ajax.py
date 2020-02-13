from xxtj.models import *
from django.http import HttpResponse, JsonResponse
import json


def add_cla_ajax(request):
    cla = class_information()
    cla.name_dis = request.GET.get('name_dis')
    cla.person_num = request.GET.get('person_num')
    cla.save()
    return JsonResponse({
        'status': 'success',
    })


def edit_cla_ajax(request):
    cla = class_information.objects.filter(isDelete=False).get(pk=request.GET.get('class_id'))
    cla.name_dis = request.GET.get('name_dis')
    cla.person_num = request.GET.get('person_num')
    cla.save()
    return JsonResponse({
        'status': 'success',
    })


def del_class_ajax(request):
    cla = class_information.objects.filter(isDelete=False).get(pk=request.GET.get('class_id'))
    cla.isDelete = True
    cla.save()
    stu = cla.student_information_set.all()
    for item in stu:
        item.isDelete = True
        item.save()
    sta = cla.statistics_information_set.all()
    for item in sta:
        rec = item.recond_set.all()
        for foo in rec:
            foo.isDelete = True
            foo.save()
        rec.isDelete = True
    return JsonResponse({
        'status': 'success',
    })


def add_stu_ajax(request):
    stu_name = request.GET.get('stu_name')
    class_id = request.GET.get('class_id')
    stu_inf = student_information()
    stu_inf.student_name = stu_name
    stu_inf.student_class = class_information.objects.filter(isDelete=False).get(pk=class_id)
    stu_inf.save()
    return JsonResponse({
        'status': 'success',
    })


def del_stu_ajax(request):
    stu_id = request.GET.get('stu_id')
    stu_inf = student_information.objects.filter(isDelete=False).get(pk=stu_id)
    stu_inf.isDelete = True
    stu_inf.save()
    return JsonResponse({
        'status': 'success',
    })


def edit_stu_ajax(request):
    stu_id = request.GET.get('stu')
    stu_inf = student_information.objects.filter(isDelete=False).get(pk=stu_id)
    stu_inf.student_name = request.GET.get('stu_name')
    stu_inf.student_class = class_information.objects.filter(isDelete=False).get(pk=request.GET.get('class_id'))
    stu_inf.save()
    return JsonResponse({
        'status': 'success',
    })


def add_sta_ajax(request):
    json_obj = request.GET.get('json')
    json_str = json.loads(json_obj)
    sta_inf = statistics_information()
    sta_inf.statistics_name = json_str["sta_name"]
    sta_inf.statistics_description = json_str["description"]
    sta_inf.statistics_class = class_information.objects.filter(isDelete=False).get(pk=json_str["class_id"])
    sta_inf.save()
    for admin_id in json_str["admin_id"]:
        adm_sta = admin_statistics()
        adm_sta.admin = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
        adm_sta.statistics = sta_inf
        adm_sta.save()
    return JsonResponse({
        'status': 'success',
    })


def add_description(json_str):
    json_str = json.loads(json_str)
    # json_str['description']
    for item in json_str['statistics']:
        sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=item)
        sta_inf.statistics_description = str(json_str['description']).replace('\n', '<br>')
        sta_inf.save()
    return JsonResponse({'status': 'success'})


def del_sta_ajax(request):
    sta_id = request.GET.get('sta_id')
    sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=sta_id)
    sta_inf.isDelete = True
    sta_inf.save()
    rec_inf = sta_inf.recond_set.all()
    for item in rec_inf:
        item.isDelete = True
        item.save()
    adm_sta_inf = sta_inf.admin_statistics_set.all()
    for item in adm_sta_inf:
        item.isDelete = True
        item.save()
    return JsonResponse({
        'status': 'success',
    })


def edit_sta_ajax(request):
    json_obj = request.GET.get('json')
    json_str = json.loads(json_obj)
    sta_id = json_str['sta']
    sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=sta_id)
    sta_inf.statistics_name = json_str['sta_name']
    sta_inf.statistics_description = json_str['sta_des']
    sta_inf.student_class = class_information.objects.filter(isDelete=False).get(pk=json_str["class_id"])
    sta_inf.save()
    adm_sta = sta_inf.admin_statistics_set.filter(isDelete=False).all()
    for item in adm_sta:
        print(item.admin)
        if item.admin.pk in json_str['admin_id']:
            try:
                obj = admin_statistics.objects.get(admin=admin_information.objects.get(pk=item.admin.pk),
                                                   statistics=statistics_information.objects.get(pk=sta_id))
                obj.isDelete = False
            except admin_statistics.DoesNotExist:
                obj = admin_statistics(admin=admin_information.objects.get(pk=item.admin.pk),
                                       statistics=statistics_information.objects.get(pk=sta_id))
            obj.save()
        else:
            obj = admin_statistics.objects.get(admin=admin_information.objects.get(pk=item.admin.pk),
                                                     statistics=statistics_information.objects.get(pk=sta_id))
            obj.isDelete = True
            obj.save()
    return JsonResponse({
        'status': 'success',
    })
