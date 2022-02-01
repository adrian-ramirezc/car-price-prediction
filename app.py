from flask import Flask, render_template, request
#import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

# app.logger.info('This is a message displayed in the terminal')

@app.route('/',methods=['GET'])
def Home():
    return render_template('home.html')


standard_to = StandardScaler()
@app.route("/", methods=['POST'])
def predict():

    Present_Price   = float(request.form['Present_Price'])
    Kms_Driven      = int(request.form['Kms_Driven'])
    Owner           = int(request.form['Owner'])
    Years_Old       = 2022 - int(request.form['Year'])
    Fuel_Type       = request.form['Fuel_Type']
    Seller_Type     = request.form['Seller_Type']
    Transmission    = request.form['Transmission']
    
    if(Fuel_Type=='Petrol'):
        Fuel_Type_Petrol=1
        Fuel_Type_Diesel=0
    elif(Fuel_Type=='Diesel'):
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=1
    else:
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=0
    
    if(Seller_Type=='Individual'):
        Seller_Type_Individual=1
    else:
        Seller_Type_Individual=0	# Dealer
    
    if(Transmission=='Mannual'):
        Transmission_Mannual=1
    else:
        Transmission_Mannual=0     # Automatic
    
    prediction  = model.predict([[Present_Price,Kms_Driven,Owner,Years_Old,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
    output      = round(prediction[0],2)
    
    if output < 0:
        return render_template('home.html',prediction_texts="Sorry, you cannot sell this car")
    else:
        return render_template('home.html',prediction_text="You can sell the car at {}".format(output))


if __name__=="__main__":
    app.run(debug=True)

