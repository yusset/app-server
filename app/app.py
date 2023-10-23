from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name)
app.secret_key = 'proyecto1-de-redes'

# Configura la conexión a la base de datos en el servidor de datos (data-server)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:_password123@10.0.0.4:5432/proyectodb'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash('Inicio de sesión exitoso')
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Error en el inicio de sesión')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
