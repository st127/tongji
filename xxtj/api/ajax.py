from ..models import statistics_information
from django.http import HttpResponse


def query_description_by_statistics(statistics):
    if statistics > 0:
        sta = statistics_information.objects.get(pk=statistics)
        description = sta.statistics_description
        return HttpResponse(description)
    else:
        return HttpResponse('请在 选择项目 中选择您要进行提交的项目')
