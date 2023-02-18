from flask import Flask, request, render_template, redirect, jsonify,url_for
from elasticsearch import Elasticsearch
import os

es = Elasticsearch({"host":"localhost","port":9200,"scheme":"http"})

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
        querytype=request.form['querytype']

        my_dir = os.path.dirname(__file__)
        file_path = os.path.join(my_dir, "elastic_search/elastic.py")
        file = open(file_path)
        getvalues={}
       
        exec(file.read(),{"query":query,"model":model, "topdocs": topdocs , "querytype" : querytype},getvalues)
    else:
        print("error occurred while making request")

    
    return render_template('result.html',query=query ,data=getvalues['data'], snippets= getvalues['snippets']) 

@app.route('/autocomplete',methods=['POST'])
def autocomplete():
    if request.method == 'POST' :
        query=request.form['data']

        result = es.search(index="sciencefiction" , body={
            "query" : {
                "multi_match" : {
                    "fields" : ["title"],
                    "query" : query ,
                    "fuzziness" : "AUTO"
                }
            }
        })

        suggestions = []

        for value in result["hits"]["hits"] :
            suggestions.append(value["_source"]["title"])

        suggestion = { "title" : suggestions }
        return suggestion 

if __name__ == "__main__":
    app.run(debug=True)

