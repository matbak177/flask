from flask import Flask, request, url_for, redirect, render_template
from datetime import datetime
import pandas as pd

ids = {
    "aaa": "mateusz.a.bak@gmail.com",
    "bbb": "kasia.h@gmail.com",
    "ddd": "franek@gmail.com"
}

df = pd.DataFrame(ids.items(), columns=['id', 'email'])

names = [
       ['mateusz.a.bak@gmail.com','Marian X', 1],
       ['mateusz.a.bak@gmail.com','Henryk P', 2],
       ['mateusz.a.bak@gmail.com','Zbycho Z', 3],
       ['mateusz.a.bak@gmail.com','Ilona B', 3],
       ['kasia.h@gmail.com','Rafal P', 4],
       ['kasia.h@gmail.com','Sandra Z',2],
       ['kasia.h@gmail.com','Mariusz B',5],
       ["franek@gmail.com", 'Stanislaw Z',6]
       ]

subordinates = pd.DataFrame(names, columns=['superior_email', 'subordinate', 'cl'])

app = Flask(__name__) 
 
@app.route('/') 
def index(): 
    return "<p>Jedziemy</p>"

@app.route('/page1/<string:id>')
def page1(id):
    email = df[df['id'] == id]['email'].values[0] if id in df['id'].values else None
    return render_template('page1.html', id=id, email=email)


@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        email = request.form['email']
        feedback_type = request.form['feedback_type']
        return render_template('page2.html',  email=email, feedback_type=feedback_type, subordinates=subordinates) # id=request.args.get('id'),
    return redirect(url_for('index'))

    
@app.route('/page3', methods=['GET', 'POST'])
def page3():
    if request.method == 'POST':
        subordinate = request.form['subordinate']
        employee = request.form.getlist('employee')
        email = request.form['email']
        feedback_type = request.form['feedback_type']
        return render_template('page3.html', email=email, feedback_type=feedback_type, subordinate=subordinate, employee=employee) 
    return redirect(url_for('index'))

if __name__ == '__main__': 
    app.run()
