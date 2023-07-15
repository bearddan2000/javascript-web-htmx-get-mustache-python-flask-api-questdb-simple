from flask import Flask
from flask_cors import CORS

import logging
from client import Endpoints

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

@app.route('/')
def smoke_test():
    smoke = {'hello': 'world'}
    return {'results': smoke}

@app.route('/dog')
def get_all():
    return {"results": client_obj.get_all()}

@app.route('/dog/color/<dog_color>')
def get_by_color(dog_color):    
    return {"results": client_obj.get_by_color(dog_color)}

@app.route('/dog/breed/<dog_breed>')
def get_by_breed(dog_breed):
    return {"results": client_obj.get_by_breed(dog_breed)}

@app.route('/dog/breed/<dog_breed>/color/<dog_color>')
def insert(dog_breed, dog_color):
    return {"results": client_obj.insert(dog_breed, dog_color)}

if __name__ == "__main__":
    client_obj = Endpoints()
    app.run(host ='0.0.0.0', port = 5000, debug = True)