from bs4 import BeautifulSoup
import requests
import csv
import mysql.connector

url = 'https://wikimon.net/Visual_List_of_Digimon'
geturl = requests.get(url)
scrap = BeautifulSoup(geturl.content, 'html.parser')
scraptable =scrap.find_all('table', style='text-align: center; width: 130px; float: left; margin: 0px 4px 2px 0px; background-color: #222222;')

# to get file digimon name in list view
digimon_name = []
digimon_link = []

# list of digimon name 
for a in scrap.find_all('table', style='text-align: center; width: 130px; float: left; margin: 0px 4px 2px 0px; background-color: #222222;'):
    for b in a.find_all('a'):
        if b.text == '':
            continue
        else:
            digimon_name.append(b.text)
        # print(digimon_name)

# list of digimon link            
for i in scrap.find_all('table', style='text-align: center; width: 130px; float: left; margin: 0px 4px 2px 0px; background-color: #222222;'):
    for y in i.find_all('img'):
        digimon_link.append('https://wikimon.net' + y['src'])
        # print(digimon_link)

# merging digimon name and link in list view
mergelist = []
z = 0
while z < len(digimon_name):
    mergelist.append([digimon_name[z], digimon_link[z]])
    z += 1
    # print(mergelist)

# save into csv file
with open('datadigimon.csv', 'w', newline = '', encoding = 'utf-8') as savefile:
    writer = csv.writer(savefile)
    writer.writerow(['digimon_name', 'digimon_link'])
    writer.writerow(mergelist)

# connect into mysql, create new database in mysql and new collection/table first
mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'Nurul',
        passwd = 'boboyuk12',
        database = 'digimon'
    )

# insert merger data into mysql
cursor = mydb.cursor()
for c in range(len(mergelist)):
    name = mergelist[c][0]
    gambar = mergelist[c][1]
    cursor.execute(
        'insert into digimon_list (name, gambar) values (%s, %s)', (name, gambar)
    )
    mydb.commit()
