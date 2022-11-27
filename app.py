from flask import Flask, request, render_template, redirect, jsonify,url_for
from elasticsearch import Elasticsearch
import json
import os


# jsonFile = open("config.json")
# config = json.load(jsonFile)

# es = Elasticsearch('https://localhost:9200')
# Elasticsearch(cloud_id = config['elasticsearch']['cloud_id'])
# api_key=(config['elasticsearch']['api_key'], config['elasticsearch'][api_keyVal])

app=Flask(__name__)

@app.route('/')
def searchQuery():
    #return data
    #can we run a python file in this?

    return render_template('search.html')

@app.route('/response', methods = ['POST','GET'])
def response():
    if request.method == 'POST':
        query=request.form['query']
        model=request.form['model']
        topdocs=request.form['topdocs']

        my_dir = os.path.dirname(__file__)
        file_path = os.path.join(my_dir, "trial.py")
        file = open(file_path)
        getvalues={}
       
        exec(file.read(),{"query":query,"model":model, "topdocs": topdocs},getvalues)
        print(getvalues)

       # print(query," ",model," ", topdocs
        
    else:
        print("error occurred while making request")

    
    return render_template('result.html',query=query ,data=getvalues['data']) 


if __name__ == "__main__":
    app.run(debug=True)
