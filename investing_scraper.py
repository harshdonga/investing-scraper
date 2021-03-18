import os
import csv
import requests
from bs4 import BeautifulSoup

if not os.path.exists('outputs'):
    os.makedirs('outputs')
os.chdir('outputs')


def create_csv(file_name, fields, rows):
    try:
        with open(file_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            writer.writerows(rows)
        print('{} Created Successfully'.format(file_name))
    except:
        print('CSV Creation Failed!')
    

def financial_overview(soup):
    tables1 = soup.find_all('table', {"class" : "common-table medium is-th-nowrap"})
    section_headers = soup.find_all('div', {"class" : "section-title js-table-title-wrapper"})
    field_names = ['Particulars', 'Values']
    rows = []
    for i in range(len(tables1)):
        body1 = tables1[i].find('tbody').find_all('tr')
        for j in body1:
            row = j.find_all('span', {'class' : 'text'})
            rows.append([row[0].text, row[1].text])

    create_csv('Financial Overview.csv', field_names, rows)


def ratios_overview():
    rows = []
    field_names = ['Particulars', 'Company', 'Industry']
    page_url = 'https://in.investing.com/equities/tata-consultancy-services-ratios'
    page_content = requests.get(page_url, headers = headers)
    page_soup = BeautifulSoup(page_content.content, 'html.parser')
    body = page_soup.find_all('tr', {"class" : "common-table-item"})[:19]
    for i in body:
        l = []
        head = i.find('td', {"class" : "col-name"})
        if head is None:
            continue
        else:
            l.append((head.text).strip())
            info = i.find_all('td', {"class" : "col-date-info"})
            for j in info:
                l.append((j.text).strip())
        rows.append(l)
    create_csv('Ratios.csv', field_names, rows)


def extract_overview(soup, file_name):
    field_names = ['Particulars']
    all_headings = soup.find_all('th')[5:10]
    for i in all_headings:
        field_names.append(i.find('span').text)
    rows = []
    all_rows = soup.find_all('tbody' , {"class" : "common-table-collapse"})
    for i in all_rows:
        l = []
        l.append((i.find('td', {"class" : "col-name"}).find('span').text).strip())
        info = i.find_all('td', {"class" : "col-date-info"})
        for j in info:
            l.append((j.text).strip())
        rows.append(l)
    create_csv(file_name+'.csv', field_names, rows)
    


base_url = 'https://in.investing.com'
tcs_url = 'https://in.investing.com/equities/tata-consultancy-services-financial-summary'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

page = requests.get(tcs_url, headers = headers)
soup = BeautifulSoup(page.content, 'html.parser')
specifics = soup.find_all('li', {"class" : "sub-tabs-item js-sub-tab-link"})
specifics_links = [i.find('a')['href'] for i in soup.find_all('li', {"class" : "sub-tabs-item js-sub-tab-link"})[1:4]]
specifics_names = [(i.text).strip() for i in soup.find_all('li', {"class" : "sub-tabs-item js-sub-tab-link"})[1:4]]



financial_overview(soup)
ratios_overview()
for i in range(len(specifics_links)):
    page_url = base_url + specifics_links[i]
    page_content = requests.get(page_url, headers = headers)
    page_soup = BeautifulSoup(page_content.content, 'html.parser')
    extract_overview(page_soup, specifics_names[i])