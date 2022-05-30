# -*- coding: utf-8 -*-

from flask import jsonify, Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from ecommerce.models import Admin
from ecommerce.jwtAuthorize import admin_login_required
import datetime
import jwt

apiAdmins = Blueprint("apiAdmins", __name__, url_prefix="/api/admins")

@apiAdmins.route("/")
@admin_login_required
def admins(current_admin):
    try:
        allAdmins = Admin.get_all_admins()
        admins = []

        for admin in allAdmins:
            admins.append(
                {
                    "id": admin.id,
                    "name": admin.name,
                    "email": admin.email,
                    "password": admin.password,
                    "mod": admin.mod,
                }
            )

        return jsonify({"data": admins, "count": len(admins)})
    except Exception as e:
        return jsonify({"success": False, "message": "There is an error.."})


@apiAdmins.route("/addAdmin", methods=["POST"])
@admin_login_required
def add_admin(current_admin):
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if name == None:
            return jsonify({"success": False, "message": "Name is required"})
        if email == None:
            return jsonify({"success": False, "message": "Email is required"})
        if password == None:
            return jsonify({"success": False, "message": "Password is required"})

        hashed_password = generate_password_hash(password)

        Admin.add_admin(name, email, hashed_password)

        return jsonify({"message": "Admin added successfully"})
    except Exception as e:
        print("ERROR in add_admin: ", e)
        return jsonify({"success": False, "message": "There is an error..", "error": e})


@apiAdmins.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
@admin_login_required
def admin(current_admin, id):
    try:
        admin = Admin.get_admin_by_id(id)

        if admin is None:
            return jsonify({"success": False, "message": "Admin not found"})

        if request.method == "GET":
            adminObj = {
                "id": admin.id,
                "name": admin.name,
                "email": admin.email,
                "password": admin.password,
            }

            return jsonify({"data": adminObj})

        # -----------------------------------------------------------------------------

        elif request.method == "DELETE":
            admin.delete_admin(id)

            return jsonify({"message": "Admin deleted"})

        # -----------------------------------------------------------------------------

        elif request.method == "PUT":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            print("NAME: ", name)
            print("EMAIL: ", email)
            print("PASSWORD: ", password)

            if name == None:
                name = admin.name
            if email == None:
                email = admin.email
            if password == None:
                password = admin.password

            hashed_password = generate_password_hash(password)

            Admin.update_admin(id, name, email, hashed_password)

            return jsonify({"message": "Admin updated"})

        # -----------------------------------------------------------------------------

    except Exception as e:
        # print("ERROR in admin: ", e)
        return jsonify({"success": False, "message": "There is an error.."})

@apiAdmins.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            print("XXXXXXXXXX")
            name = request.form.get("name")
            password = request.form.get("password")

            if name == None and password == None:
                print("yyyyyyyyy")
                return jsonify({"success": False})

            admin = Admin.get_admin_by_name(name=name)

            if admin != None:
                print("DB DEN GELEN admin IN PASSWORD U : ", admin.password)
                print("iSTEKTEN GELEN PASSWORD : ", password)

                if check_password_hash(admin.password, password):
                    print("admin id ", admin.id)

                    tokenAdmin = jwt.encode(
                        {
                            "id": admin.id,
                            "exp": datetime.datetime.utcnow()
                            + datetime.timedelta(minutes=45),
                        },
                        "ecommerce-secret",
                    )

                    session["tokenAdmin"] = tokenAdmin.decode("UTF-8")

                    admin = {"id": admin.id, "name": admin.name}

                    return jsonify({"data": admin, "tokenAdmin": tokenAdmin.decode("UTF-8")})
                else:
                    return jsonify({"error": "Passwords not matched"}), 401
            else:
                return jsonify({"error": "admin not found"}), 404
        else:
            return jsonify({"error": "This is not a Post request"}), 400
    except Exception as e:
        print("ERROR in admin login: ", e)
        return jsonify({"error": "There is an error" + str(e)})


@apiAdmins.route("/logout")
@admin_login_required
def logout(current_user):
    try:
        print("SESSION TOKEN : ", session["tokenAdmin"])
        session["tokenAdmin"] = "None"

        return jsonify({"description": "Admin Logout"})
    except Exception as e:
        return jsonify({"error": str(e)}), 502
