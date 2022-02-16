import pandas as pd
import requests
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

dispositivos = ['Google Home', 'Alexa', 'Siri homepod']
atributes = ['id','title', 'price','currency_id','available_quantity','sold_quantity','start_time','stop_time','condition','status']
df = pd.DataFrame(columns=atributes)

for disp in dispositivos:
    url = 'https://api.mercadolibre.com/sites/MLA/search?q={}&limit=50#json'.format(disp)
    response = requests.get(url)
    ids = response.json() #obtencion de ids para cada dispositivo

    for id in ids['results']:
        response = requests.get('https://api.mercadolibre.com/items/{}'.format(id['id']))
        item = response.json()

        #cargar item en dataframe
        row = {x : item[x] for x in atributes}
        df = df.append(row, ignore_index=True)

#creacion archivo csv con datos del dataframe
df.to_csv('Asistentes personales.csv',header=True, index=False)
print('Descarga exitosa.',df.shape[0],'publicaciones descargadas.')
