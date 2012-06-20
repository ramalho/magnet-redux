#!/usr/bin/env python
# coding: utf-8

import zipfile
import sys

BKP_PATH = '../../../data/bits.zip'

'''
Title: Super Mario Sunshine chega detonando para GameCube
Publisher: Magnet
Description: Game da Nintendo vende 400 mil cópias
Effective_date: 2002-07-25 17:59:55
Type: Document
Format: text/plain
Language: pt
'''

mapa_campos = {
    'Description': 'resumo', # 3088
    'Effective_date': 'dt_pub', # 7716
    'Subject': 'assunto', #  687
    'Title': 'titulo', #  7716
}
# 'Type', 'Format', 'Language', 'Publisher' tem sempre os mesmos valores:
# Document, text/plain, pt, Magnet

class EstatisticasCampo(object):
    stats = ['tamanho_max', 'amostra_max', 'tamanho_min', 'amostra_min']
    tamanho_max = 0
    tamanho_min = sys.maxsize

    def __init__(self, nome):
        self.nome = nome

    def contabilizar(self, valor):
        valor = valor.strip()
        if not valor: return  # não contar campos em branco
        if len(valor) > self.tamanho_max:
            self.tamanho_max = len(valor)
            self.amostra_max = valor
        elif len(valor) < self.tamanho_min:
            self.tamanho_min = len(valor)
            self.amostra_min = valor

    def __repr__(self):
        saida = []
        for atr in self.stats:
            valor = getattr(self, atr)
            if isinstance(valor, basestring) and len(valor) > 70:
                valor = valor[:67] + '...'
            saida.append('{0:>12}: {1}'.format(atr, valor))
        return '\n'.join(saida)


mapa_campos = {
    'Description': 'resumo', # 3088 ocorrencias
    'Effective_date': 'dt_pub', # 7716 ocorrencias
    'Subject': 'assunto', #  687 ocorrencias
    'Title': 'titulo', #  7716 ocorrencias
}
# 'Type', 'Format', 'Language', 'Publisher' tem sempre os mesmos valores:
# Document, text/plain, pt, Magnet

estatisticas = {}

def estruturar_noticia(nome, txt):
    reg = {}
    for lin in txt.split('\n'):
        lin = lin.strip()
        if not lin:
            break # fim do cabecalho
        chave, valor = lin.split(':', 1)
        if chave not in mapa_campos:
            continue # ignorar campos com valor constante
        valor = valor.strip()
        if not valor:
            continue # cabecalho em branco
        reg[chave] = valor
        stat = estatisticas.setdefault(chave, EstatisticasCampo(chave))
        stat.contabilizar(valor)
    assert reg, 'nenhum cabecalho encontrado em %r' % nome
    _, secao, ano_mes_id = nome.split('/', 2)
    reg.update(dict(secao=secao, id_orig=secao+'/'+ano_mes_id))
    return reg

with zipfile.ZipFile(BKP_PATH) as bits_zip:
    for nome in bits_zip.namelist():
        txt = bits_zip.read(nome).strip()
        if not txt: continue
        #print '*' * 80, nome
        #print txt
        reg = estruturar_noticia(nome, txt)
        #print reg

import pprint
pprint.pprint(estatisticas)
