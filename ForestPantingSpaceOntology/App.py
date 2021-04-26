from flask import Flask, render_template
import requests

app = Flask(__name__)

prefixquery = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX test: <http://www.plantingspace.com/onto#> """

@app.route('/')
def Index():
     url = 'http://localhost:3030/PSonto/sparql'
     query = prefixquery + """
             SELECT (MAX(?park_id)+1 AS ?pid) WHERE { ?x a test:Park . ?x test:ParkID ?park_id . }
                     """
     r = requests.get(url, params={'format': 'json', 'query': query})
     results = r.json()
     query1 = prefixquery + """
 SELECT (MAX(?sanctury_id)+1 AS ?sid) WHERE { ?x a test:Sanctury . ?x test:SancturyID ?sanctury_id . }
                         """
     r1 = requests.get(url, params={'format': 'json', 'query': query1})
     results1 = r1.json()

     query2 = prefixquery + """
     SELECT (MAX(?borough_id)+1 AS ?bid) WHERE { ?x a test:Borough . ?x test:BoroughID ?borough_id . }
                             """
     r2 = requests.get(url, params={'format': 'json', 'query': query2})
     results2 = r2.json()

     return render_template("index.html", data=results, data2=results2, data1=results1)


@app.route('/park')
def Park():
    title="Park"
    url = 'http://localhost:3030/PSonto/sparql'
    query = prefixquery + """ SELECT ?x ?parkname ?name ?acre ?lati ?logi ?status ?pcode WHERE
                {
                 ?x a test:Park .
                 ?x test:Name ?parkname .
                  ?x test:Acre ?acre .
                  ?x test:Latitude ?lati .
                  ?x test:Longitude ?logi .
                 ?x test:isSituatedIn ?y .
                 ?y test:Name ?name . 
                 ?y test:PostalCode ?pcode .
                 ?x test:hasStatus ?z .
                  ?z test:PSStatusValue  ?status .
                FILTER regex(?status, "", "i") 
                FILTER regex(?parkname, "", "i") 
                }
                """
    r = requests.get(url, params={'format': 'json', 'query': query})
    results = r.json()
    #print(results)
    return render_template("park.html", data=results)


@app.route('/sanctury')
def Sanctury():
    title="Park"
    url = 'http://localhost:3030/PSonto/sparql'
    query = prefixquery + """ SELECT ?x ?sancturyname ?boroghname ?acre ?htype ?status ?pcode WHERE
                {
                 ?x a test:Sanctury .
                 ?x test:Name ?sancturyname .
                  ?x test:Acre ?acre .
                  ?x test:HabitatType ?htype .
                   ?x test:isSituatedIn ?y .
                 ?y test:Name ?boroghname . 
                 ?y test:PostalCode ?pcode .
                 ?x test:hasStatus ?z .
                  ?z test:PSStatusValue  ?status .
                 ?y test:PostalCode ?pcode .
                 ?x test:hasStatus ?z .
                  ?z test:PSStatusValue  ?status .
                FILTER regex(?status, "popu", "i") 
                FILTER regex(?sancturyname, "preserve", "i") 
                FILTER regex(?htype,"forest","i")
                }
                order by ?x
                """
    r = requests.get(url, params={'format': 'json', 'query': query})
    results = r.json()
    return render_template("sanctury.html", data=results)




if __name__=="__main__":
    app.run(debug=True)