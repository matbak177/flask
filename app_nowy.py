import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import mysql.connector
from datetime import datetime

# %% Mysql
mydb = mysql.connector.connect(
    user='mateusz'
    ,password='haslo'
    ,host='localhost'
    ,database='python'
)

cursor = mydb.cursor()



# %% Logowanie
users = [
    ['mateusz.a.bak@gmail.com', 'mateuszbak', 'Mateusz Bak'],
    ['kasia.h@gmail.com', 'kasiah', 'Katarzyna H'],
    ["franek@gmail.com", 'franek', 'Franciszek Mostowiak']
]

user_df = pd.DataFrame(users, columns=['email', 'password', 'name'])

# %% Pracownicy
names = [
       ['mateusz.a.bak@gmail.com','Marian X', 1,'marian.x@gmail.com'],
       ['mateusz.a.bak@gmail.com','Henryk P', 2,'henryk.p@gmail.com'],
       ['mateusz.a.bak@gmail.com','Zbycho Z', 3,'zbycho.z@gmail.com'],
       ['mateusz.a.bak@gmail.com','Ilona B', 3,'ilona.b@gmail.com'],
       ['kasia.h@gmail.com','Rafal P', 4,'rafal.p@gmail.com'],
       ['kasia.h@gmail.com','Sandra Z',2,'sandra.z@gmail.com'],
       ['kasia.h@gmail.com','Mariusz B',5,'mariusz.b@gmail.com'],
       ["franek@gmail.com", 'Stanislaw Z',6,'stanislaw.z@gmail.com']
       ]

subordinates = pd.DataFrame(names, columns=['superior_email', 'subordinate', 'cl','email'])

# %% Aplikacja
app = Flask(__name__)

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
        return render_template('home.html', user_info=user_info, active_menu='home')
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
        return render_template('page1.html', user_info=user_info, subordinates=subordinates, active_menu='ask_for_feedback')
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

            return render_template('page2.html'
                                   , subordinates=subordinates
                                   , subordinate_cl=subordinate_cl
                                   , email=current_user
                                   , subordinate=subordinate
                                   , feedback_type=feedback_type
                                   , active_menu='ask_for_feedback'
                                   )
        
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/confirmation',methods = ['POST'])
def confirmation():
    current_user = session.get('current_user')
    if current_user:
        if request.method == 'POST':
            subordinate = request.form.get('subordinate')
            feedback_type = request.form.get('feedback_type')
    
            employees = request.form.getlist('employees')
            content = request.form.get('content')
            # employee_names = [employees.get(value, "Unknown") for value in employee_values]
            employees_split = ", ".join(employees)
            
            insert_query = '''
            INSERT INTO ask_for_feedback (timestamp, email, subordinate, feedback_type, employees, message)
            VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (datetime.now(), current_user, subordinate, feedback_type, employees_split, content))
            mydb.commit()
            
            # body = f'You want to exchange {subordinate} for {", ".join(employee_values)}'
            return render_template('page3.html'
                                   , content=content
                                   , feedback_type=feedback_type
                                   , subordinate=subordinate
                                   , employees=employees_split
                                   , current_user = current_user
                                   , active_menu='ask_for_feedback')
        return redirect(url_for('index'))

@app.route('/history') 
def history():
    current_user = session.get('current_user')
    if current_user:
        query = 'select id, timestamp, email, subordinate, feedback_type, employees, message from python.ask_for_feedback where email = "{}"'.format(current_user)
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in results]
    
        return render_template('history.html', results=results, active_menu='history')

@app.route('/edit/<int:id>', methods=['GET', 'POST']) 
def edit(id):
    if request.method == 'GET':
        # return f"<p> Tescior </p>"
        sql = '''select id, timestamp, email, subordinate, feedback_type, employees, message 
                from python.ask_for_feedback
                where id = %s'''
                
        cursor.execute(sql, [id]) 
        ask = cursor.fetchall()
        
        subordinate_cl = subordinates[subordinates['subordinate'] == ask[0][3]]['cl'].values[0]
        employee = [name.strip() for name in ask[0][5].split(',')]
        
        # columns = [col[0] for col in cursor.description]
        # asks = [dict(zip(columns, row)) for row in ask]
        
        return render_template('edit.html', id=id, active_menu='history'
                               , employee = employee
                               , subordinate_cl = subordinate_cl
                               , subordinates = subordinates
                               , ask = ask)
    else:
        return f"<p> Tescior2 </p>"
        
@app.route('/update',methods = ['POST'])
def update():
    current_user = session.get('current_user')
    if current_user:
        if request.method == 'POST':
            id = request.form.get('id')
            subordinate = request.form.get('subordinate')
            feedback_type = request.form.get('feedback_type')
            employees = request.form.getlist('employees')
            employees_split = ", ".join(employees)
            
            update_query = '''
            update python.ask_for_feedback a
            set employees = "{employees}", timestamp = "{timestamp}"
            where id = {id}
            '''.format(timestamp = datetime.now(), employees = employees_split, id = id)
 
            cursor.execute(update_query)
            mydb.commit()
            
            return render_template('update.html'
                                   , feedback_type=feedback_type
                                   , subordinate=subordinate
                                   , employees_split = employees_split
                                   , active_menu='ask_for_feedback')
        return redirect(url_for('index')) 

    
if __name__ == '__main__':
    app.secret_key = 'tutaj_wpisz'
    app.run()
