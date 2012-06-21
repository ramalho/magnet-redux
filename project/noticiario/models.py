# coding: utf-8

import datetime

from django.db import models

NIVEIS_DESTAQUE = [
        (-1, u'sem destaque'),
        (1, u'primário'),
        (2, u'secundário'),
    ]

SECOES = 'cosmonet especiais games internet mac mercado produtos'.split()
SECOES_CHOICES = zip(SECOES, SECOES)

class Noticia(models.Model):
    titulo = models.CharField(u'título', max_length=256)
    secao = models.CharField(u'seção', max_length=32, choices=SECOES_CHOICES, db_index=True)
    assunto = models.CharField(max_length=256, blank=True)
    resumo = models.CharField(max_length=256, blank=True)
    corpo = models.TextField()
    id_orig = models.CharField(max_length=64, blank=True, editable=False, db_index=True)
    publicado = models.BooleanField(db_index=True)
    dt_criacao = models.DateTimeField(u'data de criação',
        default=datetime.datetime.now, db_index=True)
    dt_atualizacao = models.DateTimeField(u'seção', editable=False, db_index=True)
    destaque = models.IntegerField(choices=NIVEIS_DESTAQUE, default=NIVEIS_DESTAQUE[0][0], db_index=True)

    class Meta:
        get_latest_by = 'dt_criacao'
        ordering = ['-dt_criacao', 'id_orig']

    def save(self, *args, **kwargs):
        '''Processar campos ao salvar'''
        self.dt_atualizacao = datetime.datetime.now()
        super(Noticia, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.titulo
