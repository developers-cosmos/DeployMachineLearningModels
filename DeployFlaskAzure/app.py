import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__,template_folder='templates')
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = [x for x in request.form.values()]
    final_features = [np.array(features)]
    column_names=['R&DSpend','Administration','MarketingSpend','State']
    final_features=pd.DataFrame(final_features,columns=column_names)
    prediction= model.predict(final_features)
    temp=0.0
    for i in prediction:
        for j in i:
            temp=j
    return render_template('index.html', prediction_text='${}'.format(temp))


if __name__ == '__main__':
	app.run(host='0.0.0.0')
