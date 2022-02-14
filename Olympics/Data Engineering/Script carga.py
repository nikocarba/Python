import pandas as pd
import numpy as np
from sqlalchemy import create_engine

athletes = pd.read_excel('Athletes.xlsx')
entriesGender = pd.read_excel('EntriesGender.xlsx')
medals = pd.read_excel('Medals.xlsx')
coaches = pd.read_excel('Coaches.xlsx')
teams = pd.read_excel('Teams.xlsx')

def lowercase_columns(df):
  '''saca las mayusculas del nombre de las columnas'''
  case_map = {col:col.lower() for col in df.columns}
  df.rename(columns=case_map, inplace=True)

lowercase_columns(athletes)
lowercase_columns(medals)
lowercase_columns(entriesGender)

mapping = {
    'Men': 'M',
    'Women': 'W',
    'Duet': 'W',
    'Team': 'W',
    'Softball': 'M',
    'Baseball': 'M',
    'Group All-Around': 'W'
}

def define_gender(event):
  if event=='Men'or event=='Women':
    return mapping[event]
  else:
    if 'Women' in event:
      return 'W'
    elif 'Men' in event:
      return 'M'
    elif 'Mixed' in event:
      return 'MW'
    else:
      try:
        return mapping[event]
      except:
        raise Exception('Not found')

genders = []
#extraigo generos de los eventos
for event in teams['Event']:
  genders.append(define_gender(event))
    
#agrego los generos como una nueva columna
teams['gender'] = genders
teams['team_id'] = teams.index #sera utilizado por la tabla duos

#separacion de duos de equipos numerosos en teams
duos = teams[teams['Name'].str.contains(r'/')][['team_id','Name']]

names = []
#separacion de integrantes de duos
for i,row in duos.iterrows():
  name1, name2 = row[1].split('/')
  names.append((row[0],name1.strip()))
  names.append((row[0],name2.strip()))
  
#generacion de tabla duos
duos_new = pd.DataFrame(names, columns=['team_id', 'name'])

#creacion nueva tabla eventos
events = teams[['Event','Discipline', 'gender']].drop_duplicates().reset_index(drop=True)
events['event_id'] = np.array(events.index).astype(str) #creacion del id
events.rename(columns={'Event':'name'}, inplace=True)
lowercase_columns(events)

#refactor de la tabla teams (se quita columnas disciplina, name y se agrega event_id)
teams_new = teams.merge(events, how='inner', left_on=['Event', 'Discipline'], right_on=['name', 'discipline'])[['team_id', 'NOC', 'event_id']]
lowercase_columns(teams_new)

#refactor de la tabla coaches (se quita columna de disciplina y se agrega event_id)
coaches_new = coaches.merge(events, how='left', left_on=['Event', 'Discipline'], right_on=['name', 'discipline'])[['Name', 'NOC', 'event_id']]
lowercase_columns(coaches_new)

#creacion de tabla dimensional comittee
noc_mapping = {x[1]:x[0] for x in enumerate(athletes['noc'].unique())} #creacion de diccionario con NOC unicos
comittees = pd.DataFrame(noc_mapping.keys(), columns=['noc'])
comittees['comittee_id'] = noc_mapping.values()
comittees = comittees.reindex(['comittee_id', 'noc'], axis=1) #cambiar orden de columnas
country_map = {
 "Islamic Republic of Iran": "Iran",
 "United States of America": "USA",
 "ROC": "Russia",
 "Federated States of Micronesia": "Micronesia",
 "Côte d'Ivoire": "Ivory Coast",
 "People's Republic of China": "China",
 "Republic of Korea": "South Korea",
 "Hong Kong, China": "China",
 "Republic of Moldova": "Moldova",
 "Lao People's Democratic Republic": "Laos",
 "Chinese Taipei": "Taiwan",
 "Democratic Republic of Timor-Leste": "Timor Leste",
 "United Republic of Tanzania": "Tanzania"
}
comittees['country'] = comittees['noc'].replace(country_map) #creacion de columna country


def modify_NOC(table, column='noc'):
  '''quita columna noc y la reemplaza por comittee_id'''
  table['comittee_id'] = table[column].map(lambda x:noc_mapping[x])
  table.drop(column, axis=1, inplace=True)

#actualizacion de NOC a comittee_id
modify_NOC(coaches_new)
modify_NOC(teams_new)
modify_NOC(athletes)
modify_NOC(medals, 'team/noc')

#insertar todas las tablas
engine = create_engine('postgresql://postgres:mossoro@localhost:5432/test')

def insert_df(df, name):
  '''inserta tabla df en la base de datos con nombre de tabla name'''
  df.to_sql(name, engine, if_exists='replace', index=False)

insert_df(duos_new, 'duos')
insert_df(coaches_new, 'coaches')
insert_df(teams_new, 'teams')
insert_df(events, 'events')
insert_df(comittees, 'comittees')
insert_df(athletes, 'athletes')
insert_df(medals, 'medals')
insert_df(entriesGender, 'genders')

print('EJECUCION EXITOSA')