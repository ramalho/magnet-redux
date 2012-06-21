# coding: utf-8

import datetime

from django.db import models

NIVEIS_DESTAQUE = [
        (-1, u'-'),
        (1, u'1'),
        (2, u'2'),
    ]

SECOES = 'cosmonet especiais games internet mac mercado produtos'.split()
SECOES_CHOICES = zip(SECOES, SECOES)

class Noticia(models.Model):
    titulo = models.CharField(u'título', max_length=256)
    secao = models.CharField(u'canal', max_length=32, choices=SECOES_CHOICES, db_index=True)
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

    def lead(self):
        if self.resumo.strip():
            return self.resumo
        else:
            if u'\r\n' in self.corpo: # tirar quebras de linhas do Windows
                self.corpo = self.corpo.replace(u'\r\n', u'\n')
                self.save()
            return self.corpo.split(u'\n\n')[0]

    @classmethod
    def secoes_existentes(cls):
        from django.db import connection
        cursor = connection.cursor()

        secoes = cursor.execute("SELECT DISTINCT secao FROM noticiario_noticia")
        secoes = (t[0] for t in secoes)

        return secoes

