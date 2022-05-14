import jwt
from functools import wraps
from flask import jsonify, request, session
from ecommerce.models import User

def admin_login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            if 'tokenAdmin' in session:
                tokenAdmin = session['tokenAdmin']
            elif 'tokenAdmin' in request.headers:
                tokenAdmin = request.headers['tokenAdmin']
            else:
                session['tokenAdmin'] = 'None'
                tokenAdmin = session['tokenAdmin']

            if tokenAdmin == 'None':
                return jsonify({'success': False, 'description': 'Please admin login the system.. 0000'}), 401

            try:
                data = jwt.decode(tokenAdmin, "ecommerce-secret")
                current_admin = User.get_user_by_id(id=data['id'])
            except:
                return jsonify({'success': False, 'description': 'Please admin login the system.. 1111'}), 401

            return f(current_admin, *args, **kwargs)
        except Exception as e:
            print("ERROR in admin_login_required: ", e)
            return jsonify({'success': False, 'description': 'Please admin login the system.. 2222'}), 401
    return decorator

def user_login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            if 'tokenUser' in session:
                tokenUser = session['tokenUser']
            elif 'tokenUser' in request.headers:
                tokenUser = request.headers['tokenUser']
            else:
                session['tokenUser'] = 'None'
                tokenUser = session['tokenUser']

            if tokenUser == 'None':
                return jsonify({'success': False, 'description': 'Please login the system.. 0000'}), 401

            try:
                data = jwt.decode(tokenUser, "ecommerce-secret")
                current_user = User.get_user_by_id(id=data['id'])
            except:
                return jsonify({'success': False, 'description': 'Please login the system.. 1111'}), 401

            return f(current_user, *args, **kwargs)
        except Exception as e:
            print("ERROR in admin_login_required: ", e)
            return jsonify({'success': False, 'description': 'Please login the system.. 2222'}), 401
    return decorator
