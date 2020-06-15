import pandas as pd
from flask import Flask, request, jsonify, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import socket
from datetime import datetime
import json
import os

#port_number = sys.argv[1]

def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        return [host_name,host_ip]
    except: 
        pass

def append(now,dictionary):
    with os.fdopen(os.open('data.json', os.O_WRONLY | os.O_CREAT, 0o600), 'a') as file:
        file.write(str('"')+now+str('":'))
        file.write(json.dumps(dictionary,indent=4))
        file.write(',')
        file.close()
        
HN,IP=get_Host_name_IP()

app = Flask(__name__,template_folder='templates')

analyser = SentimentIntensityAnalyzer()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/State',methods=['POST'])
def State():
    '''
    For rendering results on HTML GUI
    '''
    value = request.form
    # data to store
    msg = value['state']
    now = str(datetime.now())[:-7]


    features = [x for x in request.form.values()]
    text=features[0]
    result= analyser.polarity_scores(text)
    pos=round(result['pos']*100)
    neg=round(result['neg']*100)
    neu=round(result['neu']*100)
    dictionary={
        "Category":"State Government",
        "Feedback":msg,
        "Postive":pos,
        "Negative":neg,
        "Neutral":neu
    }
    append(now,dictionary)

    return render_template('index.html', prediction_text='You are {} % satisfied positively, {} % neutrally  and {} % negatively satisfied with actions of State Government'.format(pos,neu,neg),data_hn=HN,data_ip=IP)

@app.route('/Central',methods=['POST'])
def Central():
    '''
    For rendering results on HTML GUI
    '''
    value = request.form
    # data to store
    msg = value['central']
    now = str(datetime.now())[:-7]

    features = [x for x in request.form.values()]
    text=features[0]
    result= analyser.polarity_scores(text)
    pos=round(result['pos']*100)
    neg=round(result['neg']*100)
    neu=round(result['neu']*100)
    dictionary={
        "Category":"Central Government",
        "Feedback":msg,
        "Postive":pos,
        "Negative":neg,
        "Neutral":neu
    }
    append(now,dictionary)

    return render_template('index.html', prediction_text='You are {} % satisfied positively, {} % neutrally  and {} % negatively satisfied with actions of Central Government'.format(pos,neu,neg),data_hn=HN,data_ip=IP)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port = 5000, debug=True)
