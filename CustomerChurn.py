# -*- coding: utf-8 -*-
"""
	Predict Customer Churn
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	An example web application for making predicions using a saved WLM model
	using Flask and the IBM WLM APIs.

	Created by Rich Tarro
	Updated by Sidney Phoon
	May 2017
"""

import os, urllib3, requests, json
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
))

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://admin:XZLNWWMRNZHWXOCK@bluemix-sandbox-dal-9-portal.8.dblayer.com:26360/MortgageDefault'
#postgres://admin:XZLNWWMRNZHWXOCK@bluemix-sandbox-dal-9-portal.8.dblayer.com:26360/mydb
db = SQLAlchemy(app)


def predictDefault(ID,Gender,Status,Children,EstIncome,CarOwner,Age,LongDistance,International,Local,Dropped,Paymethod,LocalBilltype,LongDistanceBilltype,Usage,RatePlan):
	
	service_path = 'https://ibm-watson-ml.mybluemix.net'
	username = '87e7050e-9f43-426b-bd99-dac47c471ff2'
	password = '45cd5b72-79ae-4516-8e12-23acca895598'
	
	headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
	url = '{}/v2/identity/token'.format(service_path)
	response = requests.get(url, headers=headers)
	mltoken = json.loads(response.text).get('token')

	header_online = {'Content-Type': 'application/json', 'Authorization': "Bearer " + mltoken}
	scoring_href = 'https://ibm-watson-ml.mybluemix.net/v3/wml_instances/2d66a4d8-b28f-47c3-a667-8d7409861f75/published_models/03d74b90-b22e-4ca0-a278-aa063841d8ee/deployments/0b4e5b68-c9a0-4a20-8548-d0b63739a73d/online'
	
	payload_scoring = {
    "fields": [
    "ID",
    "Gender",
    "Status",
    "Children",
    "EstIncome",
    "CarOwner",
    "Age",
    "LongDistance",
    "International",
    "Local",
    "Dropped",
    "Paymethod",
    "LocalBilltype",
    "LongDistanceBilltype",
    "Usage",
    "RatePlan"
    ],
    "values": [ [ID,Gender,Status,Children,EstIncome,CarOwner,Age,LongDistance,International,Local,Dropped,Paymethod,LocalBilltype,LongDistanceBilltype,Usage,RatePlan] ]}
	
	response_scoring = requests.post(scoring_href, json=payload_scoring, headers=header_online)
	
	result = response_scoring.text
	print(result)
	return response_scoring


@app.route('/',  methods=['GET', 'POST'])
def index():

	if request.method == 'POST':
		ID = 999
		#Gender='F'
		#Status='S'
		#Children=0.000000
		#EstIncome=5185.310000
		#CarOwner='N'
		#Age=62.053333
		#LongDistance=16.390000
		#International=5.990000
		#Local=30.510000
		#Dropped=0.000000
		#Paymethod='CC'
		#LocalBilltype='FreeLocal'
		#LongDistanceBilltype='Intnl_discount'
		#Usage=52.900000
		#RatePlan=2.000000

		Gender=request.form['Gender']
		Status='S'
		Children=int(request.form['Children'])
		EstIncome=int(request.form['EstIncome'])
		CarOwner=request.form['CarOwner']
		Age=int(request.form['Age'])
		LongDistance=int(request.form['LongDistance'])
		International=int(request.form['International'])
		Local=int(request.form['Local'])
		Dropped=int(request.form['Dropped'])
		Paymethod=request.form['Paymethod']
		LocalBilltype='FreeLocal'
		LongDistanceBilltype='Intnl_discount'
		Usage=52.900000
		RatePlan=int(request.form['RatePlan'])
		
		
		
		session[Gender]=Gender
		session[Status]=Status
		session[Children]=Children
		session[EstIncome] = EstIncome
		session[CarOwner]=CarOwner
		session[Age]=Age
		session[LongDistance]=LongDistance
		session[International]=International
		session[Local]=Local
		session[Dropped]=Dropped
		session[Paymethod]=Paymethod
		session[LocalBilltype]=LocalBilltype
		session[LongDistanceBilltype]=LongDistanceBilltype
		session[Usage]=Usage
		session[RatePlan]=RatePlan



		response_scoring = predictDefault(ID,Gender,Status,Children,EstIncome,CarOwner,Age,LongDistance,International,Local,Dropped,Paymethod,LocalBilltype,LongDistanceBilltype,Usage,RatePlan)
		prediction = response_scoring.json()["values"][0][27]
		probability= response_scoring.json()["values"][0][26][1]

		session['prediction'] = prediction
		session['probability'] = probability

		#flash('Successful Prediction')
		return render_template('scoreSQL.html', response_scoring=response_scoring, request=request)


	else:
		return render_template('input.html')


#if __name__ == '__main__':
#   app.run()
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
