from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .api.ajax import *
from .api import ajax

# Create your views here.

def index(request, class_id):
    # return HttpResponse("This is index")
    statistics = statistics_information.objects.filter(statistics_class=class_id)
    classes = class_information.objects.get(pk=class_id)
    names = classes.student_information_set.all()
    return render(request, 'xxtj/index.html', {
        'title': 'index',
        'class_id': class_id,
        'statistics': statistics,
        'names': names,
    })


def add(request):
    requery = request.GET.get('requery')
    if requery == '0':
        statistics = request.GET.get('statistics')
        name = request.GET.get('name')
        class_id = request.GET.get('class_id')

        statistics = statistics_information.objects.get(pk=statistics)
        name = student_information.objects.get(pk=name)
        return render(request, 'xxtj/add.html', {
            'statistics': statistics,
            'name': name,
            'requery': requery,
            'class_id': class_id,
        })
    else:
        statistics = request.GET.get('statistics')              #接收GET
        name = request.GET.get('name')

        is_exists = recond.objects.all().filter(stu_id=name).exists()   #查重
        if not is_exists:
            recond_inf = recond()
            recond_inf.statistics = statistics_information.objects.get(pk=statistics)
            recond_inf.student = student_information.objects.get(pk=name)
            recond_inf.stu_id = int(name)
            recond_inf.inf = 'null'
            recond_inf.url = 'null'
        else:
            # print("********")
            recond_inf = recond.objects.get(stu_id=name)
            recond_inf.statistics = statistics_information.objects.get(pk=statistics)
            recond_inf.student = student_information.objects.get(pk=name)
            recond_inf.stu_id = int(name)
            recond_inf.inf = 'null'
            recond_inf.url = 'null'
        recond_inf.save()
        return render(request, 'xxtj/add.html', {
            'requery': '1',
            'success': '1 ',
        })



def ajax(request):
    if request.GET.get('do') == 'query_description_by_statistics':
        statistics = int(request.GET.get('statistics'))
        return query_description_by_statistics(statistics)
    # return HttpResponse("ajax worked!")


def result(request):
    return HttpResponse("This is result")
