import pandas as pd
import os

os.chdir('Ejercicios tecnicos')

#Extract
df = pd.read_excel('datasets/dataset_ejercicio1.xlsx')

#Transform
df = df[df['shipping_cost'] >0]
df['dia_mes_anio'] = df['date'].dt.strftime('%d-%m-%Y')
df['org_dest'] = df['origin_province'] + '-' + df['destination_province']
df = df.groupby(['dia_mes_anio','org_dest']).agg({'shipping_cost':['min','mean','max']}).reset_index()
df.columns = ['dia_mes_anio', 'org_dest', 'min_shipping_cost', 'avg_shipping_cost', 'max_shipping_cost']

#Load
df.to_json('output/envios.json', orient='records', force_ascii=False)