import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

# Loading the model
loaded_model = pickle.load(open("model.pkl","rb"))

# Prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,12)
    result = loaded_model.predict(to_predict)
    return result[0]

#Initializing flask
app = Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/', methods = ['POST']) # We are receiving information 
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict() # Takign the values as a dictionary
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        
        if int(result)==1:
            prediction='Income more than 50K'
        else:
            prediction='Income less that 50K'
            
        return render_template("index.html",prediction=prediction)

if __name__ == "__main__":
	app.run(debug=True)