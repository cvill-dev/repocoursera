

In the run-tests.py, look at the test case "class ApiTest(unittest.TestCase):"
there is the code to query the API. 
 
The API is coded in app.py, see def api_query_arguments()
 
You can also query the API directly in the browser via url: 
Locally 
http://127.0.0.1:7000/api_query_arguments?country=all&year=2018&month=01&day=05 
or 
via docker 
http://0.0.0.0:7000/api_query_arguments?country=all&year=2018&month=01&day=05
 
In the app.py, I also tried to develop an API using json but I have not done test on it. see def api_json() 
Obviously you have many methods to build APIs. 
https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask
I could also have used flask restful library.
https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api 