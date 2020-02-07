from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request, class_id):
    # return HttpResponse("This is index")
    return render(request, 'xxtj/index.html', {
        'title': 'index',
        'class_id': class_id,
    })


def add(request):
    statistics = request.GET.get('statistics')
    name = request.GET.get('name')
    requery = request.GET.get('requery')
    class_id = request.GET.get('class_id')
    return render(request, 'xxtj/add.html', {
        'statistics': statistics,
        'name': name,
        'requery': requery,
        'class_id': class_id,
    })


def ajax(request):
    class_id = request.GET.get('class_id')
    statistics = request.GET.get('statistics')
    # print(class_id)
    # print(statistics)
    return HttpResponse("ajax worked!")


def result(request):
    return HttpResponse("This is result")
