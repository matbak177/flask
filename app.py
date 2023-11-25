import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# %% Logowanie
users = [
    ['mateusz.a.bak@gmail.com', 'mateuszbak', 'Mateusz Bak'],
    ['kasia.h@gmail.com', 'kasiah', 'Katarzyna H'],
    ["franek@gmail.com", 'franek', 'Franciszek Mostowiak']
]

user_df = pd.DataFrame(users, columns=['email', 'password', 'name'])

# %% Pracownicy
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

# %% Aplikacja
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Sprawdź, czy istnieje taki użytkownik i czy hasło się zgadza
    user = user_df[(user_df['email'] == email) & (user_df['password'] == password)]

    if not user.empty:
        # Ustaw sesję dla zalogowanego użytkownika
        session['current_user'] = user['email'].values[0]
        return redirect(url_for('home'))
    else:
        return "Hasło niepoprawne"

@app.route('/home')
def home():
    # Sprawdź, czy użytkownik jest zalogowany
    current_user = session.get('current_user')
    if current_user:
        user_info = user_df[user_df['email'] == current_user].iloc[0]
        return render_template('home.html', user_info=user_info)
    else:
        return redirect(url_for('index'))  
    
@app.route('/ask_for_feedback')
def ask_for_feedback():
    # Sprawdź, czy użytkownik jest zalogowany
    current_user = session.get('current_user')
    if current_user:
        # Pobierz listę podwładnych z bazy danych
        # subordinates_list = subordinates[subordinates['superior_email'] == current_user]['subordinate'].tolist()
        user_info = user_df[user_df['email'] == current_user].iloc[0]
        return render_template('page1.html', user_info=user_info, subordinates=subordinates)
    else:
        return redirect(url_for('index'))  
   
@app.route('/ask_for_feedback_2', methods=['GET', 'POST'])
def ask_for_feedback_2():
    # Sprawdź, czy użytkownik jest zalogowany
    current_user = session.get('current_user')
    if current_user:
        if request.method == 'POST':
            subordinate = request.form.get('subordinate')
            feedback_type = request.form.get('feedback_type')
            
            subordinate_cl = subordinates[subordinates['subordinate'] == subordinate]['cl'].values[0]

            return render_template('page2.html', subordinates=subordinates, subordinate_cl=subordinate_cl, email=current_user, subordinate=subordinate, feedback_type=feedback_type)
        
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/history') 
def history(): 
    return f'<h1>Tu bedzie historia</h1>'

if __name__ == '__main__':
    app.secret_key = 'tutaj_wpisz'
    app.run()
    


