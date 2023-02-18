from elasticsearch import Elasticsearch
import os
import json

es = Elasticsearch({"host":"localhost","port":9200,"scheme":"http"})

custom_body = {
    "settings" : {
        "analysis" : {
            "analyzer" : {
                "custom_analyzer" : {
                    "type" : "custom" ,
                    "tokenizer" : "standard" ,
                    "filter" : ["stop" , "lowercase" , "snowball"] 
                }
            },
        }
    } ,
    

    "mappings" : {
        "properties" : {
            "paragraphs" : {
                "properties" : {
                     "text" : {
                         "type" : "text",
                     },
                     "title" : {
                         "type" : "text",
                         "fields" : {
                             "keyword" : {
                                 "type" : "keyword"
                             }
                         }
                     }
                 }
             },
             "table_of_contents" : {
                 "type" : "text",
             },
             "title" : {
                 "type" : "text",
                 "fields" : {
                     "keyword" : {
                         "type" : "keyword"
                     }
                 }
             },
             "url" : {
                 "type" : "text",
             }
             },
         }
     }


#creating index
if(not es.indices.exists(index="sciencefiction")) :
    es.indices.create(index="sciencefiction" ,body=custom_body)

    #corpus directory
    corpus_dir  = os.path.dirname(os.getcwd())+"/corpus_final"
    jsondata = []

    for files in os.listdir(corpus_dir) :
        jsonFile = open(os.path.join(corpus_dir,files))
        data = json.load(jsonFile)
        jsondata.append(data)

    # # adding documents to our index 
    for i in range(len(jsondata)) :    
        corpus_dir  = os.path.dirname(os.getcwd())+"/corpus_final"
        jsondata = []

    for files in os.listdir(corpus_dir) :
        jsonFile = open(os.path.join(corpus_dir,files))
        data = json.load(jsonFile)
        jsondata.append(data)

    # # adding documents to our index 
    for i in range(len(jsondata)) :
        es.index(id=i,index="sciencefiction",body=jsondata[i])


# changing the scoring model 
es.indices.open(index="sciencefiction")
if(model == '2') : # LMJeliner
    es.indices.close(index="sciencefiction")

    custom_settings = {
        "settings" : {
            "index": {
                "similarity" : {
                    "default" : {
                        "type" : "LMJelinekMercer"
                    }
                }
            }
        } 
    }

    es.indices.put_settings(index="sciencefiction",body=custom_settings)
else :  # model = 1 : BM25 
    es.indices.close(index="sciencefiction")

    custom_settings = {
        "settings" : {
            "index": {
                "similarity" : {
                    "default" : {
                        "type" : "BM25"
                    }
                }
            }
        } 
    }

    es.indices.put_settings(index="sciencefiction",body=custom_settings)


# since we closed index, we need to open index again to search results 
es.indices.open(index="sciencefiction")
result = {}
# query for our search
if(querytype == '1'):   #Disjunctive
    result = es.search(index="sciencefiction",size=50,body = {
        "_source" : ["title" , "url"],
        "query": {
            "multi_match" : {
                "query":query,
                "fields": [ "title^1.5", "paragraphs.text" , "paragraphs.title" ] 
            }
        },
        "highlight" : {
            "pre_tags": ["<b>"],
            "post_tags": ["</b>"], 
            "order": "score",
            "fragmenter": "simple",
            "fragment_size": 0,
            "number_of_fragments" :1,
            "fields":  {
                "paragraphs.text" : {
                    "type": "unified"
                }
            }
        }
    })
elif(querytype == '2'):     #Conjunctive : type -> best_fields
    result = es.search(index="sciencefiction",size=50,body = {
        "_source" : ["title" , "url"],
        "query": {
            "multi_match" : {
                "query":query,
                "type" : "best_fields" ,
                "fields": [ "title^1.5", "paragraphs.text" , "paragraphs.title" ] ,
                "operator" : "and"
            }
        },
        "highlight" : {
            "pre_tags": ["<b>"],
            "post_tags": ["</b>"], 
            "order": "score",
            "fragmenter": "simple",
            "fragment_size": 0,
            "number_of_fragments" :1,
            "fields":  {
                "paragraphs.text" : {
                    "type": "unified"
                }
            }
        }
    })

list=[]
snippets=[]

if((int(topdocs)) == 1) :
    if(len(result["hits"]["hits"]) < 7) :
        number = len(result["hits"]["hits"])
    else :
        number = 7
elif ((int(topdocs)) == 2) :
    if(len(result["hits"]["hits"]) < 10) :
        number = len(result["hits"]["hits"])
    else :
        number = 10
elif((int(topdocs)) == 3) :
    number = len(result["hits"]["hits"])

if(len(result["hits"]["hits"]) == 0) :  # no results found
    number = 0

for i in range(number) :
    list.append(result["hits"]["hits"][i]["_source"]["url"]) 
    
    for key in result["hits"]["hits"][i]:
        if(key == "highlight"):
            snippets.append(result["hits"]["hits"][i][key]["paragraphs.text"][0])
            

data= list
snippets = snippets


