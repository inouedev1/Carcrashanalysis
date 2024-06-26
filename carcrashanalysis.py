# -*- coding: utf-8 -*-
"""Carcrashanalysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17ZUSFwB4AnxUQ_A1e8noB67RZB33EiEz
"""

import json

import pandas as pd

import warnings
warnings.filterwarnings('ignore')

path = "/content/monroe county car crach 2003-2015.csv"

df = pd.read_csv(path, encoding='latin1')

"""Monroe County é um ESTADO DE NOVA YORQUE"""

df

df.columns

df = df.drop(columns=['Latitude','Longitude','Reported_Location',])

df = df.reset_index()
df.rename(columns={'index': 'Casos'}, inplace=True)
df

import plotly.express as px
grafico_casos_ano = px.histogram(df, x='Year',
nbins=20, title='Numero de casos por ano',
labels={'Year': 'Ano', 'Casos': 'Número de Casos'})
grafico_casos_ano

df['Weekend?'] = df['Weekend?'].replace({'Weekday': 'Dia de semana', 'Weekend': 'Final de semana'})

grafico_casos_semana = px.histogram(df, x='Weekend?',
nbins=20, title='Numero de casos por em dia da semana ou final',
labels={'Weekend?': 'Semana/Final de semana', 'count': 'Número de Casos'})
grafico_casos_semana

grafico_casos_hora = px.histogram(df, x='Hour',
nbins=20, title='Numero de casos em horario do dia',
labels={'Hour' : 'Casos/Hora do dia', 'count': 'Número de Casos'})
grafico_casos_hora

df['Injury Type'] = df['Injury Type'].replace({'No injury/unknown': 'Sem ferimentos/desconhecido', 'Non-incapacitating': 'Acidentes Leves', 'Incapacitating' : 'Acidentes Graves', 'Fatal' : 'Acidentes fatais'})

grafico_casos_ferimento = px.histogram(df, x='Injury Type',
nbins=20, title='Numero de casos por tipo de ferimento',
labels={'Injury Type': 'Casos/Tipo de ferimento', 'count': 'Número de Casos'})
grafico_casos_ferimento

grafico_ferimento_porcentagem = px.pie(df, names='Injury Type', title='Porcentagem de Casos por Tipo de Ferimento')

grafico_ferimento_porcentagem.show()

fatores_unicos = df['Primary Factor'].unique()
#print(fatores_unicos)

df['Primary Factor'] = df['Primary Factor'].replace({'OTHER (DRIVER) - EXPLAIN IN NARRATIVE': 'OUTROS(MOTORISTA) - EXPLICADO NO BO',
    'FOLLOWING TOO CLOSELY': 'DIRIGINDO MUITO PROXIMO A OUTRO CARRO',
    'DISREGARD SIGNAL/REG SIGN': 'IGNORAR SINAL/SINALIZAÇÃO REGULAMENTAR',
    'FAILURE TO YIELD RIGHT OF WAY': 'FALHA AO CEDER A PREFERÊNCIA',
    'DRIVER DISTRACTED - EXPLAIN IN NARRATIVE': 'MOTORISTA DISTRAÍDO',
    'ENGINE FAILURE OR DEFECTIVE': 'FALHA OU DEFEITO NO MOTOR',
    'RAN OFF ROAD RIGHT': 'SAÍDA DE PISTA À DIREITA',
    'UNSAFE BACKING': 'RÉ INDEVIDA',
    'ROADWAY SURFACE CONDITION': 'MÁ CONDIÇÃO DA PISTA',
    'nan': 'N/A',
    'SPEED TOO FAST FOR WEATHER CONDITIONS': 'VELOCIDADE MUITO ALTA PARA AS CONDIÇÕES CLIMÁTICAS',
    'ANIMAL/OBJECT IN ROADWAY': 'ANIMAL/OBJETO NA VIA',
    'PEDESTRIAN ACTION': 'AÇÃO DO PEDESTRE',
    'IMPROPER TURNING': 'VIRADA IMPRÓPRIA(FECHAR O OUTRO MOTORISTA)',
    'UNSAFE LANE MOVEMENT': 'MOVIMENTO DE FAIXA INSEGURO',
    'LEFT OF CENTER': 'À ESQUERDA DO CENTRO DA PISTA',
    'IMPROPER LANE USAGE': 'USO IMPRÓPRIO DA FAIXA',
    'OVERCORRECTING/OVERSTEERING': 'REACAO EXCESSIVA',
    'BRAKE FAILURE OR DEFECTIVE': 'FALHA OU DEFEITO NOS FREIOS',
    'UNSAFE SPEED': 'VELOCIDADE INSEGURA',
    'DRIVER ASLEEP OR FATIGUED': 'MOTORISTA DORMINDO OU FATIGADO',
    'VIEW OBSTRUCTED': 'VISÃO OBSTRUÍDA',
    'DRIVER ILLNESS': 'MOTORISTA DOENTE',
    'IMPROPER PASSING': 'ULTRAPASSAGEM IMPRÓPRIA',
    'OTHER (VEHICLE) - EXPLAIN IN NARRATIVE': 'OUTRO (VEÍCULO)',
    'OTHER (ENVIRONMENTAL) - EXPLAIN IN NARR': 'OUTRO (AMBIENTAL)',
    'WRONG WAY ON ONE WAY': 'CONTRAMÃO EM VIA DE MÃO ÚNICA',
    'ACCELERATOR FAILURE OR DEFECTIVE': 'FALHA OU DEFEITO NO ACELERADOR',
    'INSECURE/LEAKY LOAD': 'CARGA INSEGURA/VASANDO',
    'CELL PHONE USAGE': 'USO DE CELULAR',
    'TIRE FAILURE OR DEFECTIVE': 'FALHA OU DEFEITO NO PNEU',
    'OTHER TELEMATICS IN USE': 'OUTROS APARELHOS ELETRONICOS',
    'HEADLIGHT DEFECTIVE OR NOT ON': 'FAROL DEFEITUOSO OU DESLIGADO',
    'OTHER LIGHTS DEFECTIVE': 'OUTRAS LUZES DEFEITUOSAS',
    })

df

grafico_casos_causa_histo = px.histogram(df, x='Primary Factor',
nbins=20, title='Numero de casos por causa',
labels={'Primary Factor': 'Casos/Fatores', 'count': 'Número de Casos'})
grafico_casos_causa_histo

casos_por_fator = df['Primary Factor'].value_counts().reset_index()
casos_por_fator.columns = ['Primary Factor', 'Count']
total_casos = casos_por_fator['Count'].sum()
casos_por_fator['Percentage'] = (casos_por_fator['Count'] / total_casos) * 100
grafico_casos_causa_pizza = px.pie(
    casos_por_fator,
    names='Primary Factor',
    values='Percentage',
    title='Porcentagem de Casos por Causa'
)
grafico_casos_causa_pizza.show()

fatores_maior_4 = casos_por_fator[casos_por_fator['Percentage'] >= 4].copy()
fatores_menor_4 = casos_por_fator[casos_por_fator['Percentage'] < 4].copy()
outros_casos = pd.DataFrame({
    'Primary Factor': ['Outros Casos'],
    'Count': [fatores_menor_4['Count'].sum()],
    'Percentage': [fatores_menor_4['Percentage'].sum()]
})
casos_agrupados = pd.concat([fatores_maior_4, outros_casos], ignore_index=True)
grafico_casos_causa_mais4 = px.pie(
    casos_agrupados,
    names='Primary Factor',
    values='Percentage',
    title='Porcentagem de Casos por Causa (acima de 4%)'
)
grafico_casos_causa_mais4.show()

casos_alcool = df[df['Primary Factor'] == 'ALCOHOLIC BEVERAGES'].shape[0]
casos_nao_alcool = df[df['Primary Factor'] != 'ALCOHOLIC BEVERAGES'].shape[0]
data = {
    'Primary Factor': ['Casos de Motorista Embriagado', 'Casos de Motorista Não Embriagado'],
    'Count': [casos_alcool, casos_nao_alcool]
}
df_comparacao = pd.DataFrame(data)
total_casos = df_comparacao['Count'].sum()
df_comparacao['Percentage'] = (df_comparacao['Count'] / total_casos) * 100
grafico_comparacao = px.pie(
    df_comparacao,
    names='Primary Factor',
    values='Percentage',
    title='Comparação de Casos: Motorista Embriagado vs. Não Embriagado'
)
grafico_comparacao.show()