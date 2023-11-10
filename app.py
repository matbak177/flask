from flask import Flask, request, url_for
from datetime import datetime

app = Flask(__name__) 
 
@app.route('/') 
def index(): 
    return '<h1>Hello World</h1>'

@app.route('/cantor/<currency>/<amount>')
def cantor(currency, amount):
    message = f'<h1>You selected {currency} and amount {amount}</h1>'
    return message

@app.route('/about') 
def about(): 
    return '<h1>We are progremmers</h1>'
    
if __name__ == '__main__':
    app.run()
