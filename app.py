from flask import Flask, request, render_template, redirect, jsonify,url_for
from elasticsearch import Elasticsearch
import json
import requests
import os
from flask_restful import Api , Resource , reqparse


# jsonFile = open("config.json")
# config = json.load(jsonFile)

es = Elasticsearch({"host":"localhost","port":9200,"scheme":"http"})
# Elasticsearch(cloud_id = config['elasticsearch']['cloud_id'])
# api_key=(config['elasticsearch']['api_key'], config['elasticsearch'][api_keyVal])

app=Flask(__name__)
api = Api(app)

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
        # print(getvalues)

        #print(query," ",model," ", topdocs)
        
    else:
        print("error occurred while making request")

    
    return render_template('result.html',query=query ,data=getvalues['data']) 






# class Controller(Resource):
#     def __init__(self):
#         self.query = parser.parse_args().get("query", None)
#         self.baseQuery ={
#             "_source": [],
#             "size": 0,
#             "min_score": 0.5,
#             "query": {
#                 "bool": {
#                     "must": [
#                         {
#                             "match_phrase_prefix": {
#                                 "title": {
#                                     "query": "{}".format(self.query)
#                                 }
#                             }
#                         }
#                     ],
#                     "filter": [],
#                     "should": [],
#                     "must_not": []
#                 }
#             }
#                 }

#     def get(self):
#         res = es.search(index="finalindex0", size=0, body=self.baseQuery)
#         return res


# parser = reqparse.RequestParser()
# parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

# api.add_resource(Controller, '/autocomplete')




# @app.route('/pipe', methods=["GET", "POST"])
# def pipe():
#     data = request.form.get("data")
#     payload = {}
#     headers= {}
#     url = "http://127.0.0.1:4000/autocomplete?query="+str(data)
#     response = requests.request("GET", url, headers=headers, data = payload)
#     return response.json()
# # #------------------------------------#
@app.route('/autocomplete',methods=['POST'])
def autocomplete():
    if request.method == 'POST' :
        query=request.form['data']

        # es.indices.close(index="finalindex0")

        # custom_settings = {
        #     "settings" : {
        #         "index": {
        #             "similarity" : {
        #                 "default" : {
        #                     "type" : "BM25"
        #                 }
        #             }
        #         }
        #     } 
        # }

        # es.indices.put_settings(index="finalindex0",body=custom_settings)
        # es.indices.open(index="finalindex0")
        print(query)

        result = es.search(index="finalindex0" , body={
            "query" : {
                "fuzzy" : {
                    "title" : {
                        "value" : query ,
                        "fuzziness" : "AUTO"
                    }
                }
            }
        })

        
        print("\n\n")
        # print(result)
        print("\n\n")

        suggestions = []

        for value in result["hits"]["hits"] :
            suggestions.append(value["_source"]["title"])

        suggestion = { "title" : suggestions }
        return suggestion 




# required_args = reqparse.RequestParser()
# required_args.add_argument('data' , type=str , required=True , help="Query is required" , location='form')

# class AutoComplete(Resource) :
#     def get(self) :
#         args = request.form.get("query")
#         print("\n\n")
#         print("Hello")
#         print(args)

#         result = es.search(index="finalindex0",
#                             body = { "query": {
#                                         "fuzzy" : {
#                                             "title": {
#                                                 "value" : args['data'],
#                                                 "fuzziness" : "AUTO"
#                                             }
#                                         }
#                                     }})

#         return result

# api.add_resource(AutoComplete , "/autocomplete")


# class Controller(Resource):
#     def __init__(self):
#         self.query = parser.parse_args().get("query", None)
#         self.baseQuery ={
#             "query": {
#                     "fuzzy" : {
#                         "title": {
#                             "value" : "{}".format(self.query),
#                             "fuzziness" : "AUTO"
#                         }
#                     }
#             }
#         }

#     def get(self):
#         res = es.search(index="finalindex0", body=self.baseQuery)
#         return res


# parser = reqparse.RequestParser()
# parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

# api.add_resource(Controller, '/autocomplete')

# @app.route('/pipe', methods=["GET", "POST"])
# def pipe():
#     data = request.form.get("data")
#     payload = {}
#     headers= {}
#     url = "/autocomplete?query="+str(data)
#     response = requests.request("GET", url, headers=headers, data = payload)
#     return response.json()


if __name__ == "__main__":
    app.run(debug=True)
