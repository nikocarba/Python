import requests
from bs4 import BeautifulSoup
import pandas as pd

page = 0
def extract(page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    url = f'https://www.hotcourseslatinoamerica.com/study/training-degrees/international/subject/data/sin/ct/programs.html#search&keyword=DATA&localsearchkeyword=data&nationCode=174&nationCntryCode=174&studyAbroad=N&studyOnline=N&studyCross=N&studyDomestic=N&studyPartTime=N&startOnlineCampusLater=N&manStdyAbrdFlg=N&restRefineFlag=Y&pageNo={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    cookies = r.cookies
    return soup, cookies

def transform(soup):
    divs = soup.find_all('div', class_ = 'pr_rslt')
    for div in divs:
        title = div.find('div', class_ = 'sr_nam').a.text.strip()
        location = div.find('span', class_ ='grey').text
        link = div.find('a', class_ = 'whpd_clk')['href']

        job = {
            'title':title,
            'location':location,
            'link':link}
        joblist.append(job)

    return 

def aditional_info(jobs):
    for item in jobs:
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
        url = item[2]
        r = requests.get(url, headers, cookies=cookies)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        careers = soup.find_all('div', class_ = 'pr_hd')

        for career in careers:
            name = career.find('div', class_ = 'sr_nam').h2.text
            valor = career.find_all('div', class_ = 'pr_hd_rgt')[-1].text.strip()
            if '$' not in valor:
                valor='-'

            curso = {
                'University':item[0],
                'Carrera': name,
                'Valor': valor,
                'Pais': item[1]
            }
            carreras.append(curso)
    return

joblist = []
carreras = []

for i in range(0, 50, 1):
    soup, cookies = extract(i)
    transform(soup)

df_universities = pd.DataFrame(joblist)
df_universities.drop_duplicates(inplace=True)
universidades = df_universities.values.tolist()

aditional_info(universidades)

df = pd.DataFrame(carreras)

df.to_csv('carreras.csv', index=False)

print('EJECUCION EXITOSA.', df.shape[0],'carreras de data descargadas.')
#print('Unique values', len(df.title.unique()))
#print('Number of jobs:', len(joblist))