import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.preprocessing import StandardScaler
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3 as sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Steller_prediction.db'

# Initilize the database
db = SQLAlchemy(app)

# Create db model class
class Steller_prediction_db(db.Model):
    date_created = db.Column(db.DateTime,default=datetime.utcnow, primary_key = True)
    ra = db.Column(db.Float, nullable=False)
    dec = db.Column(db.Float, nullable=False)
    u = db.Column(db.Float, nullable=False)
    g = db.Column(db.Float, nullable=False)
    r = db.Column(db.Float, nullable=False)
    i = db.Column(db.Float, nullable=False)
    z = db.Column(db.Float, nullable=False)
    redshift = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.String(200), nullable=False)
    # Create a function to return string when we add some thing
    def __repr__(self):
        return '<date_created %r>' % self.date_created

# Load model from a pickel file
model = pickle.load(open('LogisticRegression_Model.pkl','rb'))

# route to home page
@app.route('/')
def home():
    return render_template('index.html')

# route to view database entries
@app.route('/tables')
def table():
    # connect to database
    con = sql.connect("Steller_prediction.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    # execute query
    cur.execute("select * from Steller_prediction_db")
   
    rows = cur.fetchall(); 
    return render_template("table.html", rows = rows)

@app.route('/predict',methods=["POST"])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    print(int_features)
    input_df = pd.DataFrame(int_features)
   
    x = StandardScaler().fit(input_df).transform(input_df).squeeze()

    prediction = model.predict(np.array( [x.squeeze(),]))

    steller_prediction = ""
    if prediction[0] == 0:
        steller_prediction = " Galaxy"
    if prediction[0] == 1:
        steller_prediction = " QSO"
    if prediction[0] == 2:
        steller_prediction = " Star"

    if request.method == "POST":
        print("In request")
        # print(request.form)
        dt = datetime.now()
        ra = request.form['ra']
        dec = request.form['dec']
        u = request.form['u']
        g = request.form['g']
        r = request.form['r']
        i = request.form['i']
        z = request.form['z']
        redshift = request.form['redshift']
        prediction = steller_prediction
        steller_obj = Steller_prediction_db(date_created=dt, ra=ra, dec=dec, u=u, g=g, r=r, i=i, z=z, redshift=redshift , prediction=prediction)
        
        try:
            db.session.add(steller_obj)
            db.session.commit()
            
        except:
            return "There was an error add steller information"
    return render_template("index.html", prediction_text = "Steller belongs to class: {}".format(steller_prediction))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)