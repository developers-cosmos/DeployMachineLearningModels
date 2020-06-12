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
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    result=0.0
    for i in prediction:
        for j in i:
            result=j

    return render_template('index.html', prediction_text='Employee Salary should be $ {:.2f}'.format(result*100))


if __name__ == '__main__':
	app.run(port = 5000, debug=True)
