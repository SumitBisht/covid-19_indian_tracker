from bs4 import BeautifulSoup
import requests
import json
import os
from flask import Flask, render_template

app = Flask(__name__)
def savetofile(key, data):
    key = 'data/'+key
    if os.path.isfile(key):
        return
    else:
        f = open(key, "w")
        f.write(str(data))
        f.close()
        return

def scrape():
    base_url = "https://www.mohfw.gov.in/"
    get = requests.get(base_url)
    soup = BeautifulSoup(get.text, "html.parser")
    state_Data = []
    tb = soup.findAll('table', class_='table')[-1]
    data_upload_time = soup.select_one(".newtab").findChildren("strong", recursive=True)[0].string
    key = (data_upload_time.split()[5]+'_'+data_upload_time.split()[7]).replace(':','')

    for tr in tb.find_all('tr'):
        if(tr.find_all("td")):
            cols = tr.find_all("td")
            if(len(cols)==5):
                state_Data.append({
                    "serial":"total",
                    "state":"Totals",
                    "cases":cols[1].text,
                    "foreign":cols[2].text,
                    "cured":cols[3].text,
                    "death":cols[4].text
                })
            elif(len(cols)==6):
                state_Data.append({
                    "serial":cols[0].text,
                    "state":cols[1].text,
                    "cases":cols[2].text,
                    "foreign":cols[3].text,
                    "cured":cols[4].text,
                    "death":cols[5].text
                })
    result = json.dumps(state_Data)
    savetofile(key, result)
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/js/<filename>')
def serverJS(filename):
    return render_template(filename)

@app.route('/data')
def data():
    return scrape()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
