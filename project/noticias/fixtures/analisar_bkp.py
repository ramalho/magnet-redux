#!/usr/bin/env python
# coding: utf-8

import zipfile

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

# qt_campos_cabecalho = {}
valores_campos_cabecalho = {}

def estruturar_noticia(nome, txt):
    reg = {}
    for lin in txt.split('\n'):
        lin = lin.strip()
        if not lin:
            break # fim do cabecalho
        chave, valor = lin.split(':', 1)
        valor = valor.strip()
        if not valor:
            continue # cabecalho em branco
        reg[chave] = valor
        # qt_campos_cabecalho[chave] = qt_campos_cabecalho.get(chave, 0) + 1
        valores = valores_campos_cabecalho.setdefault(chave, set())
        if len(valores) < 10:
            valores.add(valor)
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
pprint.pprint(valores_campos_cabecalho)