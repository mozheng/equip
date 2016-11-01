from django.conf.urls import include,url
import django.views.static
import main.views

urlpatterns = [
    url(r'^css/(?P<path>.*)$', django.views.static.serve, {'document_root': 'static\css'}),
    url(r'^js/(?P<path>.*)$', django.views.static.serve, {'document_root': 'static\js'}),
    url(r'^images/(?P<path>.*)$', django.views.static.serve, {'document_root': 'static\images'}),
    url(r'^fonts/(?P<path>.*)$', django.views.static.serve, {'document_root': 'static\fonts'}),
    url(r'^data/(?P<path>.*)$', django.views.static.serve, {'document_root': 'static\data'}),

    ########my views##
    url(r'^DegradationOfBearings.html$', main.views.visual, name='visual'),
    url(r'^DegradationOfBearings.html(?P<file>\w+)$', main.views.visual, name='file'),

]
