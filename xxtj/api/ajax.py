from ..models import statistics_information
from django.http import HttpResponse


def query_description_by_statistics(statistics):
    sta = statistics_information.objects.get(pk=statistics)
    description = sta.statistics_description
    return HttpResponse(description)
