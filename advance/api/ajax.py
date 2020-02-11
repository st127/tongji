from xxtj.models import *
from django.http import HttpResponse, JsonResponse




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
    sta_inf = statistics_information()
    sta_inf.statistics_name = request.GET.get('sta_name')
    sta_inf.statistics_description = request.GET.get('sta_des')
    sta_inf.statistics_class = class_information.objects.filter(isDelete=False).get(pk=request.GET.get('class_id'))
    sta_inf.save()
    return JsonResponse({
        'status': 'success',
    })


def del_sta_ajax(request):
    sta_id = request.GET.get('sta_id')
    sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=sta_id)
    sta_inf.isDelete = True
    sta_inf.save()
    rec_inf = sta_inf.recond_set.all()
    for item in rec_inf:
        item.isDelete = True
        item.save()
    return JsonResponse({
        'status': 'success',
    })


def edit_sta_ajax(request):
    sta_id = request.GET.get('sta')
    sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=sta_id)
    sta_inf.statistics_name = request.GET.get('sta_name')
    sta_inf.statistics_description = request.GET.get('sta_des')
    sta_inf.student_class = class_information.objects.filter(isDelete=False).get(pk=request.GET.get('class_id'))
    sta_inf.save()
    return JsonResponse({
        'status': 'success',
    })
