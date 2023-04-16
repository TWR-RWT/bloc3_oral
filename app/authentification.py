#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from app import app, request, render_template, flash, redirect, url_for, session, get_db, token_required_auth, jwt, datetime, timedelta, generate_password_hash, check_password_hash
import os
import psycopg2
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
import os
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask import jsonify
from flask import session
import jwt
from functools import wraps
from jinja2 import Template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


@app.route('/users', methods=['POST']) ###############ok
#@token_required_auth
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        hashed_password = generate_password_hash(request.form['password'], method='sha256')
        role = request.form['role']
        print(f"username: {username}")
        print(f"hashed_password: {hashed_password}")
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO mercadona.accounts (name, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
                    conn.commit()
                    cur.close()#
                    #conn.close()#
            flash('Compte créée avec succès')
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash('Erreur lors de la création du compte')
            return redirect(url_for('index'))







@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                        SELECT * FROM mercadona.accounts 
                        WHERE name = %s
                    """, (username,))
                user = cur.fetchone()
                #conn.commit()
                cur.close()#
                #conn.close()#
                if check_password_hash(user[2], password):
                    token = jwt.encode({'user': user[1], 'exp': datetime.utcnow() + timedelta(hours=24)}, app.config['SECRET_KEY'])
                    session['username'] = username
                    session['logged_in'] = True
                    session['token'] = token
                    session['user_id'] = user[0]
                    session['role'] = user[3]
                    return redirect(url_for('index'))
                else:
                    flash('Nom d\'utilisateur ou mot de passe incorrect')
    return render_template('/authentification/login.html')






@app.route("/logout")
def logout():
    session.clear()
    flash('Vous avez été déconnecté')
    return redirect(url_for('index'))

@app.route("/connexion")
def connexion():
    return render_template('/authentification/login.html')









##### Page Comptes #####
@app.route("/comptes")
@token_required_auth
def comptes():
    return render_template('/authentification/comptes.html')
