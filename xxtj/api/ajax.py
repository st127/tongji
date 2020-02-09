from ..models import *
from django.http import HttpResponse, JsonResponse
import json

from django.shortcuts import render
import json


def query_description_by_statistics(statistics):
    sta = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
    description = sta.statistics_description
    return HttpResponse(description)


def add_recond(statistics, stu_id):
    is_exists = recond.objects.all().filter(isDelete=False).filter(stu_id=stu_id).exists()  # 查重
    if not is_exists:
        recond_inf = recond()
        recond_inf.statistics = statistics_information.objects.get(pk=statistics)
        recond_inf.student = student_information.objects.filter(isDelete=False).get(pk=stu_id)
        recond_inf.stu_id = int(stu_id)
        recond_inf.inf = 'null'
        recond_inf.url = 'null'
    else:
        # print("********")
        recond_inf = recond.objects.filter(isDelete=False).get(stu_id=stu_id)
        recond_inf.statistics = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
        recond_inf.student = student_information.objects.filter(isDelete=False).get(pk=stu_id)
        recond_inf.stu_id = int(stu_id)
        recond_inf.inf = 'null'
        recond_inf.url = 'null'
    recond_inf.save()
    stat = {
        'status': 'success',
    }
    return JsonResponse(stat)


def get_result_by_sta(statistics):
    sta = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
    reconds = sta.recond_set.all().filter(isDelete=False)
    stu_inf_all = sta.statistics_class.student_information_set.all()
    # print(reconds)
    # print(stu_inf_all)
    stu_statistical = {}
    stu_unstatistical = {}
    stu_reconded =[]
    l_sta = 0
    l_unsta = 0
    for items in reconds:
        l_sta = l_sta + 1
        stu_statistical[l_sta] = "<tr><td>" + stu_inf_all.filter(isDelete=False).get(pk=items.stu_id).student_name + "</tr></td>"
        stu_reconded.append(items.stu_id)
    for items in stu_inf_all:
        if items.pk not in stu_reconded:
            l_unsta = l_unsta + 1
            stu_unstatistical[l_unsta] = "<tr><td>" + stu_inf_all.filter(isDelete=False).get(pk=items.pk).student_name + "</tr></td>"
    # print(stu_statistical)
    # print(stu_unstatistical)
    sent_dic = {
        'description': sta.statistics_description,
        'l_sta': l_sta,
        'l_unsta': l_unsta,
        'statistical': stu_statistical,
        'unstatistical': stu_unstatistical,
    }
    return JsonResponse(sent_dic)


def clear_sta(statistics):
    sta = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
    reconds = sta.recond_set.all()
    for items in reconds:
        items.isDelete = True
        items.save()
    return JsonResponse({'status': 'success'})


def add_description(json_str):
    json_str = json.loads(json_str)
    # json_str['description']
    for item in json_str['statistics']:
        sta_inf = statistics_information.objects.get(pk=item)
        sta_inf.statistics_description = json_str['description']
        sta_inf.save()
    return JsonResponse({'status': 'success'})
