# import dependencies
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

# to run on flask 
# run prompt, navigate to same folder, then enter
# set FLASK_APP=app.py
# then enter 
# flask run
# go to the http local host 
