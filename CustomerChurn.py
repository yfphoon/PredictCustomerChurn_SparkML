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
	username = 'db7336ae-b258-4b0c-9bd2-57ca9d090f08'
	password = 'ff129993-058d-472b-bbcb-edf40568b6c8'

	headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
	url = '{}/v2/identity/token'.format(service_path)
	response = requests.get(url, headers=headers)
	mltoken = json.loads(response.text).get('token')
	header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
	scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/3194"
	payload_scoring = ({"record":[ID,Gender,Status,Children,EstIncome,CarOwner,Age,LongDistance,International,Local,Dropped,Paymethod,LocalBilltype,LongDistanceBilltype,Usage,RatePlan]})
	response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
	
	result = response_scoring.text
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

		prediction = response_scoring.json()["result"]["prediction"]
		probability = response_scoring.json()["result"]["probability"]["values"][1]

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
