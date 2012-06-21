# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from noticiario.models import Noticia

import json
import pprint
import datetime

CAMPOS_BKP = [u'assunto', u'secao', u'resumo', u'id_orig', u'titulo', u'corpo', u'dt_pub']

class Command(BaseCommand):
    args = '<arquivo_backup.json>'
    help = 'Carrega os dados do backup da Magnet'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Informe o nome do arquivo .json com o backup da Magnet')
        self.stdout.write('Abrindo %s\n' % args[0])
        with open(args[0]) as bkp_json:
            bkp = json.load(bkp_json)
        self.stdout.write('%s noticias lidas\n' % len(bkp))
        for num, noticia_bkp in enumerate(bkp, 1):
            noticia_bkp['dt_criacao'] = datetime.datetime.strptime(
                            noticia_bkp['dt_pub'], '%Y-%m-%d %H:%M:%S')
            del noticia_bkp['dt_pub']
            noticia = Noticia(**noticia_bkp)
            noticia.save()
            if num % 100 == 0:
                self.stdout.write('%s noticias salvas\n' % num)

        #self.stdout.write(pprint.pformat(noticia_bkp)+'\n')
        self.stdout.write('%s noticias salvas\n' % num)

'''
Conforme cat /proc/cpuinfo, o computador onde este script foi feito tem
"Intel(R) Pentium(R) Dual CPU T3400 @ 2.16GHz" rodando 4321.88 bogomips.
O tempo de execução foi 21 minutos para 7716 notícias salvas no Sqlite3:

$ time ./manage.py carga ../data/bits.json
Abrindo ../data/bits.json
7716 noticias lidas
100 noticias salvas
200 noticias salvas
...
7600 noticias salvas
7700 noticias salvas
7716 noticias salvas

real    21m17.169s
user    0m14.561s
sys 0m9.565s

Depois este script foi testado em um MacBook Pro (2011) com "Intel Core i7
Dual @ 2.7 GHz" e o resultado foi:

7600 noticias salvas
7700 noticias salvas
7716 noticias salvas

real    1m52.988s
user    0m8.956s
sys 0m6.691s


'''