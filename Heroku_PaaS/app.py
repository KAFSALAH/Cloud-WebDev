from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # initializing the app

ENV = 'prod'
if ENV == 'dev':
        app.debug = True # Devolopment stage
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0000@localhost/lexus'
    
else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mwynoadtdwnmro:b9a123075f44b5b59e1a88e1fe760ae58edf8cd5808094747308242f8ceeeb08@ec2-3-227-68-43.compute-1.amazonaws.com:5432/d5s8j0to8l2c87'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Turn off warnings

db = SQLAlchemy(app) # Create a database object
class Feedback(db.Model):
    __tablename__ ='feedback'
    id = db.Column(db.Integer, primary_key = True) # defining fields 
    customer = db.Column(db.String(200), unique = True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())
    # define an initializer to the class
    def __init__ (self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments
        

    

@app.route('/') # making a route 
def index():
    return render_template('index.html') # What will opens in the mian page

# To handle post submits
@app.route('/submit', methods= ['POST'])
def submit():
    if request.method == 'POST': # To ensure it is a post method
        customer = request.form['customer'] # customer is the name of the field used in the html
        dealer = request.form['dealer'] # these are the names in the form of index.html
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message ='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer ==customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message ='You have already submitted your feedback')


if __name__ == '__main__':
    app.run()