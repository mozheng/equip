from django.shortcuts import render

from django.template import RequestContext, loader
from django.shortcuts import Http404, render_to_response, get_object_or_404
from django.http import HttpResponse


# Create your views here.


def fisher(request):
    return render_to_response('echarts/fisher.html')

def visual(request):
    try:
        view = ""
        file = ""
        para= ""
        if 'file' in request.GET and request.GET['file']:
            #print "GET file:"
            name = request.GET['file']
            if 'para' in request.GET and request.GET['para']:
                para = request.GET['para']
            file = "echarts/" + name + ".html"
            if file!="":
                 view =  'main'
    except Exception as e:
        print e
    return render_to_response('program/DegradationOfBearings.html', RequestContext(request, {
        'file': file,
        'para': para,
        'view': view,
    }))
