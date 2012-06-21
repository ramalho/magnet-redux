# coding: utf-8

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .models import Noticia

def menu_secoes(secao_ativa=None):
    return (dict(nome=secao, classe=('active' if secao==secao_ativa else ''))
            for secao in Noticia.secoes_existentes())

class HomePageView(TemplateView):

    template_name = 'noticiario/fluid.html'

    def get_context_data(self, **kwargs):
        secao = kwargs.get('secao')
        context = super(HomePageView, self).get_context_data(**kwargs)
        try:
            destaques = Noticia.objects.filter(destaque=1)
            if secao:
                destaques = destaques.filter(secao=secao)
            destaque = destaques.latest()
        except Noticia.DoesNotExist:
            destaque = {'titulo':u'Nenhum destaque primário encontrado',
                        'lead':u'Use o admin para designar uma notícia'
                                 u' como destaque primário. O destaque'
                                 u' primário mais recente aparece aqui',
                        'pk': 0}
        context['destaque'] = destaque
        resultado = Noticia.objects.filter(destaque=2)
        if secao:
            resultado = resultado.filter(secao=secao)
        resultado = resultado.order_by('dt_criacao')[:12]
        context['destaques_secundarios'] = (resultado[i:i+3] for i in range(0, len(resultado), 3))
        context['secoes'] = menu_secoes(secao)
        return context
