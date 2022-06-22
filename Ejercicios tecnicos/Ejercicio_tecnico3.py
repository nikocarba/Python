import pandas as pd
import datetime as dt
import pyodbc

time = dt.datetime.now().strftime('%Y-%m-%d')
filename = 'carga_{}.log'.format(time)
f = open(f'Python/ejercicios tecnicos/logs/{filename}', 'w') #Archivo de logs
f.write('LOGS\n')
f.write('-----------\n\n')

#Extract
url = 'https://adlschallenge.blob.core.windows.net/challenge/nuevas_filas.csv?sp=r&st=2022-06-20T14:51:53Z&se=2022-12-31T22:51:53Z&spr=https&sv=2021-06-08&sr=b&sig=y9hLJFCVvGh1Ej58SXqsXTSVC6ABoVuQgfECDOd83Lw%3D'
try:
    df = pd.read_csv(url)
except:
    f.write('{} - No se pudo descargar el archivo.\n'.format(dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
if df.shape[0] == 0:
    f.write('{} - Archivo vacio.\n'.format(dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
    exit()

#Transform
df.dropna(subset=['ID', 'MUESTRA', 'RESULTADO'], inplace=True) #dropea filas con keys nulos
df.drop_duplicates(['ID', 'MUESTRA', 'RESULTADO'], keep='last', inplace=True) #dropea los duplicados
df['FECHA_COPIA'] = dt.datetime.now() #pobla el campo FECHA_COPIA con la fecha y hora de carga
registros = len(df)


#Load
conn = pyodbc.connect(
    'Driver=ODBC Driver 17 for SQL Server;'
    'Server=desktop;'
    'Database=challenge;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

try:
    cursor.executemany(f"INSERT INTO prueba VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", df.values.tolist())
    conn.commit()
    f.write('{} - {} registros cargados.\n'.format(dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), registros))
except:
    f.write('{} - Falla en el proceso no se cargó ningun registro.\n'.format(dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))

#Verificar que no hubo perdida de informacion
cursor.execute('SELECT count(*) FROM prueba where fecha_copia = (select max(fecha_copia) from prueba)') #extraigo la cantidad de registros cargados en BD
f.write('{} - Se perdieron {} registros.\n'.format(dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), registros - cursor.fetchone()[0])) #comparo los registros descargados contra los cargados en BD

f.close()
cursor.close()