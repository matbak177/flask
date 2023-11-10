from flask import Flask, request, render_template
import pandas as pd
import mysql.connector
import pymysql
import os

class SendMail():
    
    def __init__(self,query):
        self.query=query
        
    @staticmethod    
    def MySQLConnect():
        mydb = mysql.connector.connect(
            user='mateusz'
            ,password=''
            ,host='localhost'
            
            ,database='python'
        )
    
        return mydb
    
    def read_data(self):
        df = pd.read_sql_query(self.query,self.MySQLConnect())
        return df
            
df = SendMail('Select * from team').read_data()

dict= {}
for i,j in zip(df['email'], df['name']):
    
    dict[i] = j
    
    print(i, j)

print(dict)

options_names = {
    "option1": "Opcja 1",
    "option2": "Opcja 2",
    "option3": "Opcja 3",
    "option4": "Opcja 4",
    "option5": "Opcja 5",
    "option6": "Opcja 6",
    "option7": "Opcja 7",
}

app = Flask(__name__) 

@app.route('/') 
def index(): 

    return '<h1>Druga strona: {}</h1>'.format('test')  

@app.route('/proby/<string:email>')
def proby(email):
    
    return render_template("start.html", email=email)
    # return render_template("zaczynamy.html", email=email)


@app.route('/confirmation',methods = ['POST'])
def confirmation():
    
    subordinate = request.form['subordinate']
    # subordinate = options_names.get(request.form['subordinate'], "Unknown")
    
    employee_values = request.form.getlist('employee')
    employee_names = [options_names.get(value, "Unknown") for value in employee_values]
        
    # body = f'You want to exchange {subordinate} for {", ".join(employee)}'
    body = f'You want to exchange {subordinate} for {", ".join(employee_names)}'

    return body


if __name__ == '__main__':
    app.run()
