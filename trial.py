from elasticsearch import Elasticsearch
import os
import json
print("\n\n")
print("model:" , model)
print("\n\n")


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
            "links" : {
                 "type" : "text",
            },
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
if(not es.indices.exists(index="finalindex")) :
    es.indices.create(index="finalindex0" ,body=custom_body)

    #corpus directory
    corpus_dir  = os.getcwd()+"/corpus"
    jsondata = []

    for files in os.listdir(corpus_dir) :
        jsonFile = open(os.path.join(corpus_dir,files))
        data = json.load(jsonFile)
        jsondata.append(data)

    # # adding documents to our index 
    for i in range(len(jsondata)) :    
        corpus_dir  = os.getcwd()+"/corpus"
        jsondata = []

    for files in os.listdir(corpus_dir) :
        jsonFile = open(os.path.join(corpus_dir,files))
        data = json.load(jsonFile)
        jsondata.append(data)

    # # adding documents to our index 
    for i in range(len(jsondata)) :
        es.index(id=i,index="finalindex0",body=jsondata[i])


# changing the scoring model 
if(model == '2') : # LMJeliner
    es.indices.close(index="finalindex0")

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

    es.indices.put_settings(index="finalindex0",body=custom_settings)
else :  # model = 1 : BM25 default -> no need to change type
    es.indices.close(index="finalindex0")

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

    es.indices.put_settings(index="finalindex0",body=custom_settings)


# since we closed index, we need to open index again to write queries    
es.indices.open(index="finalindex0")

# query for our search
result = es.search(index="finalindex0",body = {
    "query": {
        "multi_match" : {
            "query":query,
            "fields": [ "title", "paragraphs.text" ] ,
        }
    }
})

list=[]

if((int(topdocs)) == 1) :
    number = 7
elif ((int(topdocs)) == 2) :
    number = 10
elif((int(topdocs)) == 3) :
    if(len(result["hits"]["hits"])) >= 20 :
        number = 20
    else :
        number = len(result["hits"]["hits"])

for i in range(number) :
    list.append(result["hits"]["hits"][i]["_source"]["url"]) 
    list.append(result["hits"]["hits"][i]["_score"])

data= list



#for i in range(0,100):
#    jsonFile = open(os.path.join(corpus_dir,(os.listdir(corpus_dir))[i]))
#    data = json.load(jsonFile)
#    jsondata.append(data)

#for i in range(100) :
#    es.index(id=i,index="finalindex",body=jsondata[i])

