from flask import jsonify, Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt

from ecommerce.models import User
from ecommerce.jwtAuthorize import admin_login_required, user_login_required

apiUsers = Blueprint("apiUser", __name__, url_prefix="/api/users")

@apiUsers.route("/")
@admin_login_required
def users(current_admin):
    try:
        allUsers = User.get_all_users()
        users = []

        for user in allUsers:
            users.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "activated": user.activated,
                }
            )

        return jsonify({"data": users, "count": len(users)})
    except Exception as e:
        # print("ERROR in users: ", e)
        return jsonify({"message": "There is an error.."}), 502

@apiUsers.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
@admin_login_required
def user(current_admin, id):
    try:
        user = User.get_user_by_id(id)

        if user is None:
            return jsonify({"message": "User not found"}), 404

        if request.method == "GET":
            userObj = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
            }

            return jsonify({"data": userObj})

        # -----------------------------------------------------------------------------

        elif request.method == "DELETE":
            user.delete_user(id)

            return jsonify({"message": "User deleted"})

        # -----------------------------------------------------------------------------

        elif request.method == "PUT":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            print("USERNAME: ", username)
            print("EMAIL: ", email)
            print("PASSWORD: ", password)

            if username == None:
                username = user.username
            if email == None:
                email = user.email
            if password == None:
                password = user.password

            hashed_password = generate_password_hash(password)

            User.update_user(id, username, email, hashed_password)

            return jsonify({"message": "User updated"})

        # -----------------------------------------------------------------------------

    except Exception as e:
        # print("ERROR in user: ", e)
        return jsonify({"message": "There is an error.."}), 502

@apiUsers.route("/addUser", methods=["POST"])
def addUser():
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        print("USERNAME: ", username)
        print("EMAIL: ", email)
        print("PASSWORD: ", password)

        if username == None or email == None or password == None:
            return jsonify({"message": "Missing fields"}), 422

        hashed_password = generate_password_hash(password)

        print("HASHED PASSWORD: ", hashed_password)

        User.add_user(username, email, hashed_password)

        return jsonify({"message": "User added successfully.."})
    except Exception as e:
        print("ERROR in addUser: ", e)
        return jsonify({"message": "There is an error"}), 502


@apiUsers.route("activate_user", methods=["POST"])
@admin_login_required
def activateUser(current_admin):
    try:
        id = request.form.get("id")
        user = User.get_user_by_id(id)

        if user is None:
            return jsonify({"message": "User not found"}), 404

        if user.activated == True:
            return jsonify({"message": "User already activated"}), 400

        User.activate_user(id)

        return jsonify({"message": "User activated"})
    except Exception as e:
        print("ERROR in activateUser: ", e)
        return jsonify({"message": "There is an error"}), 502


@apiUsers.route("deactivate_user", methods=["POST"])
@admin_login_required
def deactivateUser(current_admin):
    try:
        id = request.form.get("id")
        user = User.get_user_by_id(id)

        if user is None:
            return jsonify({"message": "User not found"}), 404

        if user.activated == False:
            return jsonify({"message": "User already deactivated"}), 400

        User.deactivate_user(id)

        return jsonify({"message": "User deactivated"})
    except Exception as e:
        print("ERROR in deactivateUser: ", e)
        return jsonify({"message": "There is an error"}), 502


@apiUsers.route("deactiveusers", methods=["GET"])
@admin_login_required
def deactiveUsers(current_admin):
    try:
        allUsers = User.get_all_users()
        users = []

        for user in allUsers:
            if user.activated == False:
                users.append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "password": user.password,
                        "activated": user.activated,
                    }
                )

        return jsonify({"data": users, "count": len(users)})
    except Exception as e:
        print("ERROR in deactiveUsers: ", e)
        return jsonify({"message": "There is an error.."}), 502


@apiUsers.route("activeusers", methods=["GET"])
@admin_login_required
def activeUsers(current_admin):
    try:
        allUsers = User.get_all_users()
        users = []

        for user in allUsers:
            if user.activated:
                users.append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "password": user.password,
                        "activated": user.activated,
                    }
                )

        return jsonify({"data": users, "count": len(users)})
    except Exception as e:
        print("ERROR in activeUsers: ", e)
        return jsonify({"message": "There is an error.."}), 502

@apiUsers.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            print("XXXXXXXXXX")
            username = request.form.get("username")
            password = request.form.get("password")

            if username == None and password == None:
                print("yyyyyyyyy")
                return jsonify({"success": False})

            user = User.get_user_by_username(username=username)

            if user != None:
                print("DB DEN GELEN USER IN PASSWORD U : ", user.password)
                print("İSTEKTEN GELEN PASSWORD : ", password)

                if check_password_hash(user.password, password):
                    print("user ıd ", user.id)

                    tokenUser = jwt.encode(
                        {
                            "id": user.id,
                            "exp": datetime.datetime.utcnow()
                            + datetime.timedelta(minutes=45),
                        },
                        "ecommerce-secret",
                    )

                    session["tokenUser"] = tokenUser.decode("UTF-8")

                    user = {"id": user.id, "username": user.username}

                    return jsonify({"data": user, "tokenUser": tokenUser.decode("UTF-8")})
                else:
                    return jsonify({"error": "Passwords not matched"}), 401
            else:
                return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"error": "This is not a Post request"}), 400
    except Exception as e:
        print("ERROR in user login: ", e)

        return jsonify({"error": "There is an error.."}), 502


@apiUsers.route("/logout")
@user_login_required
def logout(current_user):
    try:
        print("SESSION TOKEN : ", session["tokenUser"])
        session["tokenUser"] = "None"

        return jsonify({"description": "User Logout"})
    except Exception as e:
        return jsonify({"error": str(e)}), 502

@apiUsers.route("/profile", methods=["GET", "DELETE", "PUT"])
@user_login_required
def profile(current_user):
    try:
        user = current_user

        if user is None:
            return jsonify({"message": "User not found"}), 404

        if request.method == "GET":
            userObj = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
            }

            return jsonify({"data": userObj})

        # -----------------------------------------------------------------------------

        elif request.method == "DELETE":
            user.delete_user(user.id)

            return jsonify({"message": "User deleted"})

        # -----------------------------------------------------------------------------

        elif request.method == "PUT":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            print("USERNAME: ", username)
            print("EMAIL: ", email)
            print("PASSWORD: ", password)

            if username == None:
                username = user.username
            if email == None:
                email = user.email
            if password == None:
                password = user.password

            hashed_password = generate_password_hash(password)

            User.update_user(user.id, username, email, hashed_password)

            return jsonify({"message": "User updated"})

        # -----------------------------------------------------------------------------

    except Exception as e:
        # print("ERROR in user: ", e)
        return jsonify({"message": "There is an error.."}), 502
