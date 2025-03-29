from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['first_name'].strip()
        apellido = request.form['last_name'].strip()
        email = request.form['email'].lower().strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        accept_terms = request.form.get('accept_terms') == 'on'

        # Validaciones
        if not all([nombre, apellido, email, password, confirm_password]):
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('auth.registro'))

        if not accept_terms:
            flash('Debes aceptar los términos y condiciones', 'danger')
            return redirect(url_for('auth.registro'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.registro'))

        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'danger')
            return redirect(url_for('auth.registro'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Email no válido', 'danger')
            return redirect(url_for('auth.registro'))

        try:
            # Verificar si el email ya existe
            cur = mysql.connection.cursor()
            cur.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
            if cur.fetchone():
                flash('Este email ya está registrado', 'danger')
                return redirect(url_for('auth.registro'))

            # Insertar nuevo usuario
            hashed_pw = generate_password_hash(password)
            cur.execute(
                "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)",
                (nombre, apellido, email, hashed_pw)
            )
            mysql.connection.commit()
            cur.close()

            flash('¡Registro exitoso! Por favor inicia sesión', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            mysql.connection.rollback()
            flash('Error en el servidor: ' + str(e), 'danger')

    return render_template('auth/registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username'].lower().strip()
        password = request.form['password']

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                session['user_name'] = f"{user['nombre']} {user['apellido']}"
                flash(f'¡Bienvenido/a {user["nombre"]}!', 'success')
                return redirect(url_for('general.inicio'))
            else:
                flash('Email o contraseña incorrectos', 'danger')

        except Exception as e:
            flash('Error en el servidor: ' + str(e), 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('general.inicio'))