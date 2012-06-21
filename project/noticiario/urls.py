from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .views import HomePageView
from .models import Noticia

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'bits/(?P<pk>\d+)/', DetailView.as_view(model=Noticia), name='noticia-detail')
)
