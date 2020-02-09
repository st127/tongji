from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .api.ajax import *
from .api import ajax


# Create your views here.


def index(request, class_id):
    # return HttpResponse("This is index")
    statistics = statistics_information.objects.filter(statistics_class=class_id)
    classes = class_information.objects.filter(isDelete=False).get(pk=class_id)
    names = classes.student_information_set.all()
    return render(request, 'xxtj/index.html', {
        'title': 'index',
        'class_id': class_id,
        'statistics': statistics,
        'names': names,
    })


def add(request):
    statistics = request.GET.get('statistics')
    name = request.GET.get('name')
    class_id = request.GET.get('class_id')
    statistics = statistics_information.objects.get(pk=statistics)
    name = student_information.objects.get(pk=name)
    return render(request, 'xxtj/add.html', {
        'statistics': statistics,
        'name': name,
        'class_id': class_id,
        })


def ajax(request):
    do = request.GET.get('do');
    if do is None:
        return HttpResponse("Format Error!")
    if do == 'query_description_by_statistics':
        statistics = int(request.GET.get('statistics'))
        return query_description_by_statistics(statistics)
    if do == 'add_recond':
        statistics = int(request.GET.get('statistics'));
        stu_id = int(request.GET.get('stu_id'));
        return add_recond(statistics, stu_id);
    if do == 'get_result_by_sta':
        statistics = int(request.GET.get('statistics'));
        return get_result_by_sta(statistics)
    if do == 'clear_sta':
        statistics = int(request.GET.get('statistics'));
        return clear_sta(statistics)


def result(request):
    admin_id = request.GET.get('admin_id')
    if admin_id is None:
        return render(request, 'xxtj/result.html')
    else:
        adm_sta = admin_information.objects.filter(isDelete=False).get(pk=int(admin_id))
        adm_sta = adm_sta.admin_statistics_set.all()
        statistics = {}
        for items in adm_sta:
            statistics[items.statistics.pk] = items.statistics.statistics_description
        # print(statistics)
        return render(request, 'xxtj/result.html', {
            'statistics': statistics,
        })
