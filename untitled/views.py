from django.shortcuts import render, Http404, render_to_response, get_object_or_404
from django.template import RequestContext, loader
import os
from devices.models import Devices
from devices.models import Program


def index(request):
    return render_to_response('index.html')


def single(request):
    Dev = {}
    print "####"
    if 'device' in request.GET and request.GET['device']:
        dev_name = request.GET['device']
        Dev = Devices.objects.filter(name=dev_name)

        return render_to_response('single.html', RequestContext(request, {
        'device': Dev[0],
        }))
    else:
        return render_to_response('sale.html')

def sale(request):
    return render_to_response('sale.html')


def fisher(request):
    return render_to_response('echarts/fisher.html')


