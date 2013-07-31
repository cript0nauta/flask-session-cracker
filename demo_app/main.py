#-*- coding: utf-8 -*-

from flask import Flask, redirect, url_for, render_template, session, request
app = Flask(__name__)
app.debug = True
app.secret_key='bigsecret'
#app.config['SESSION_COOKIE_HTTPONLY'] = False # Para debugear

users = [
        ('guest', 'guest', False),
        ('admin', 'd5f4sd56f4sd56f54f56sd7f89sd7fsd2g14gf5hjg6f', True),
        ]

@app.route('/')
def index():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = request.form.get('username')
        pwd = request.form.get('pwd')
        if (user, pwd, True) in users:
            session['usuario'] = user
            session['admin'] = True
            return redirect(url_for('index'))
        elif (user, pwd, False) in users:
            session['usuario'] = user
            session['admin'] = False
            return redirect(url_for('index'))
        else:
            return render_template('login.html', e='Datos incorrectos')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()


