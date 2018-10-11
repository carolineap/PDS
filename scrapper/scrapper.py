#author: Gabriel Eiji Uema Martin

from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
import json
import sys

URL = ''

class Ajuste:
    vencimento = None
    ajuste_anterior = None
    ajuste_atual = None
    variacao = None
    ajuste_contrato = None

    def __init__(self, vencimento, ajuste_anterior, ajuste_atual, variacao, ajuste_contrato):
        self.vencimento = vencimento.strip(' ')
        self.ajuste_anterior = ajuste_anterior.strip(' ')
        self.ajuste_atual = ajuste_atual.strip(' ')
        self.variacao = variacao.strip(' ')
        self.ajuste_contrato = ajuste_contrato.strip(' ')

class Mercadoria:
    nome = None
    ajustes = []

    def __init__(self, nome, ajustes):
        self.nome = nome.strip(' ')
        self.ajustes = ajustes

class Requisicao:
    data = None
    mercadorias = []

    def __init__(self, data):
        print("Iniciando requisição para %s" % data)
        self.data = data
        self.mercadorias = self.request_mercadorias()

    # Faz o request da tabela para a URL dada, faz o parsing e retorna as mercadorias
    def request_mercadorias(self):

        tabela = self.request_table(URL)

        if tabela is None:
            return None

        mercadorias = self.parse_table(tabela)

        if mercadorias is None:
            return None

        return mercadorias

    # Faz o request para a URL dada e retorna a tabela de ajustes diários do dia dado
    def request_table(self, url):
        r = requests.post(url=url, data={'dData1': self.data})
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup.find('table', attrs={'id': 'tblDadosAjustes'})

    # Faz o parse da tabela dada e retorna uma lista de mercadorias com seus ajustes
    def parse_table(self, table):
        rows = table.find_all('tr')

        mercadorias = []

        for i in range (1, len(rows)):

            colunas = rows[i].find_all('td')

            vencimento = colunas[1].text
            ajuste_anterior = colunas[2].text
            ajuste_atual = colunas[3].text
            variacao = colunas[4].text
            ajuste_contrato = colunas[5].text

            ajuste = Ajuste(vencimento, ajuste_anterior, ajuste_atual, variacao, ajuste_contrato)

            if len(colunas[0].text) == 0:
                mercadorias[-1].ajustes.append(ajuste)
            else:
                mercadorias.append(Mercadoria(colunas[0].text, [ajuste]))

        return mercadorias

    # Retorna requisições para um range de datas
    def request_batch(start_date, end_date = None):
        date_format = '%d/%m/%Y'

        start = datetime.strptime(start_date, date_format)
        end = datetime.strptime(end_date, date_format)

        step = timedelta(days=1)

        requisicoes = []

        while(start <= end):
            requisicoes.append(Requisicao(start.strftime(date_format)))
            start+= step

        return requisicoes