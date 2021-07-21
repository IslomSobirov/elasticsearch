from flask import Flask
from flask.globals import request
from flask import json
import mysql.connector
import requests

app = Flask(__name__)
# app.run(debug=True, host='0.0.0.0', port=5000)

mydb = mysql.connector.connect(
        host="185.74.5.8",
        user="bitrix_admin",
        password="1658761b",
        database="express_db_2020_08_04"
    )

searchRoute = "localhost:9200"

@app.route('/')
def hello_world():

    return {
        "message": "Hellow"
    }

@app.route('/blogs', methods=['GET', 'POST'])
def blogs():
    if request.method == 'POST':
        title = request.json["title"]
        body = request.json["body"]

        query = "INSERT INTO blog_b (title, body) values ('{}', '{}')"
        query = query.format(title, body)
        
        cursor = mydb.cursor()
        cursor.execute(query)

        # id = cursor.execute("SELECT LAST_INSERT_ID() as id")
        # id = id.fetchall()

        # requests.post("/blog/_doc/1", json={
        #     "title": title,
        #     "body": body
        # })

        return {
            "message": "Created Successfuly!"
        }
    else:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM blog_b order by id desc limit 10")
        records = cursor.fetchall()
        listToreturn = []

        for item in records:
            items = {
                "id": item[0],
                "title": item[1],
                "body": item[2]
            }
            listToreturn.append(items)
    

        return json.jsonify(listToreturn)
@app.route('/blogs/<int:blog_id>', methods=['PUT'])
def updateBlog(blog_id):

    title = request.json["title"]
    body = request.json["body"]

    query = "UPDATE blog_b set title = '{}', body = '{}' where id = {}"
    query = query.format(title, body, blog_id)
    
    cursor = mydb.cursor()
    cursor.execute(query)

    route = "http://elasticsearch:9200/blog/_doc/{}"
    route = route.format(blog_id)

    requests.post(route, json={
        "title": title,
        "body": body
    })


    return {
        "message": "Successfully updated"
    }

@app.route('/search')
def seaerch():
    word = request.json["query"]

    jsonForRequest = {
        "query": {
            "bool": {
            "should": [
                {"match": {"title": word}}, 
                {"match": {"body": word}}
            ]
            }
        },
        "highlight" : {
            "fields" : {
                "title" : {},
                "body": {}
            }
        }
    }
    
    route = "http://elasticsearch:9200/blog/_search"
    responses = requests.get(route, json=jsonForRequest).json()
    responses = dict(responses)
    hits = responses["hits"]["hits"]

    jsonToReturn = []
    for hit in hits:
        obj = {}
        if hit["highlight"].get("body") != None:
            obj["body"] = hit["highlight"]["body"][0]
        if hit["highlight"].get("title") != None:
            obj["title"] = hit["highlight"]["title"][0]
        jsonToReturn.append(obj)
                

    return json.jsonify(jsonToReturn)
        

