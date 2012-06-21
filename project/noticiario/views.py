# coding: utf-8

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .models import Noticia

class HomePageView(TemplateView):

    template_name = 'noticiario/fluid.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            destaque = Noticia.objects.filter(destaque=1).latest()
        except Noticia.DoesNotExist:
            destaque = {'titulo':u'Nenhum destaque primário encontrado',
                        'resumo':u'Use o admin para designar uma notícia'
                                 u' como destaque primário. O destaque'
                                 u' primário mais recente aparece aqui',
                        'pk': 0}
        context['destaque'] = destaque
        resultado = Noticia.objects.filter(destaque=2).order_by('dt_criacao')[:12]
        context['destaques_secundarios'] = ((resultado[i:i+3]) for i in range(0, len(resultado), 3))
        return context
