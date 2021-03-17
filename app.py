
from flask import Flask, jsonify, request, render_template, make_response
import joblib
import socket
import json
import pandas as pd
import os
import modelTool

MODEL_DIR = "models"
DATA_DIR = "data"

app = Flask(__name__)

@app.route("/")
def hello():
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/predict', methods=['GET', 'POST'])

def main():
    if request.method == 'GET':
        return(render_template('main.html'))
    if request.method == 'POST':
        country = request.form['country']
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']   
        prediction = modelTool.model_predict(country,year,month,day) 
        return render_template('main.html',
                                     original_input={'Country':country,
                                                     'Year':year,
                                                     'Month':month,
                                                     'Day':day,
                                                     },
                                     result=prediction,
                                     )
 
 
@app.route('/api_json', methods=['POST'])
def api_json():

    request_data = request.get_json()

    country = None
    year = None
    month = None
    day = None

    if request_data:
        if 'country' in request_data:
           # if len(request_data['country']) > 0:
           country = request_data['country']

        if 'year' in request_data:
            year = request_data['year']
        
        if 'month' in request_data:
            month = request_data['month']

        if 'day' in request_data:
            framework = request_data['day']
                
    return '''
           The country value is: {}
           The year value is: {}
           The month version is: {}
           The day value is: {}'''.format(country, year, month, day)

 
@app.route('/api_query_arguments')
def api_query_arguments():

    # https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
    # Test url:
    # http://127.0.0.1:7000/api_query_arguments?country=all&year=2018&month=01&day=05

    country = request.args.get('country')
    month = request.args['month']
    year = request.args.get('year')
    day = request.args.get('day')
    print('''
           The country value is: {}
           The year value is: {}
           The month version is: {}
           The day value is: {}'''.format(country, year, month, day))
           
    
    #return '''
    #       The country value is: {}
    #       The year value is: {}
    #       The month version is: {}
    #       The day value is: {}'''.format(country, year, month, day)
     
    prediction = modelTool.model_predict(country,year,month,day)
    print(prediction)
    return jsonify(prediction)
     
if __name__ == '__main__':
    # host 127.0.0.1 if i run locally on windows without docker
    #app.run(host='127.0.0.1', port=7000,debug=True)
    # host 0.0.0.0 if i run in a docker container
    app.run(host='0.0.0.0', port=7000,debug=True)
