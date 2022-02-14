import pandas as pd
import requests
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

dispositivos = ['Google%20Home', 'Alexa', r'Siri%20homepod']
atributes = ['id','title', 'price','currency_id','available_quantity','sold_quantity','start_time','stop_time','condition','status']
df = pd.DataFrame(columns=atributes)

for disp in dispositivos:
    url = 'https://api.mercadolibre.com/sites/MLA/search?q={}&limit=50#json'.format(disp)
    response = requests.get(url)
    a = response.json()        
    for id in a['results']:
        response = requests.get('https://api.mercadolibre.com/items/{}'.format(id['id']))
        a = response.json()

        row = {x : a[x] for x in atributes}
        df = df.append(row, ignore_index=True)

df.to_csv('Asistentes personales.csv',header=True, index=False)
print('Descarga exitosa.',df.shape[0],'dispositivos descargados.')
