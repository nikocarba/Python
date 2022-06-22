import pandas as pd
import datetime as dt
import pyodbc


#Extract
url = 'https://adlschallenge.blob.core.windows.net/challenge/nuevas_filas.csv?sp=r&st=2022-06-20T14:51:53Z&se=2022-12-31T22:51:53Z&spr=https&sv=2021-06-08&sr=b&sig=y9hLJFCVvGh1Ej58SXqsXTSVC6ABoVuQgfECDOd83Lw%3D'
try:
    df = pd.read_csv(url)
except:
    print('No se pudo descargar el archivo.')
if df.shape[0] == 0:
    print('Archivo vacio.')
    exit()

#Transform
df.drop_duplicates(['ID', 'MUESTRA', 'RESULTADO'], keep='last', inplace=True) #dropea los duplicados
df['FECHA_COPIA'] = dt.datetime.now() #pobla el campo FECHA_COPIA con la fecha y hora de carga


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
    print(f'{len(df)} rows inserted to the prueba table.')
except:
    print('Falla en el proceso no se cargó ningun registro.')

cursor.execute('SELECT count(*) FROM prueba')
cursor.fetchone()[0]

cursor.close()