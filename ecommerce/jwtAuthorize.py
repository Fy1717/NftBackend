import jwt
from functools import wraps
from flask import jsonify, request, session
from ecommerce.models import User

def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            if "token" in session or "token" in request.headers:
                if "token" in session:
                    print("-------token in session-------")
                    token = session["token"]
                    print("token session --> ", token)

                if "token" in request.headers:
                    print("-------token in headers-------")
                    token = request.headers["token"]
                    print("token headers --> ", token)
            else:
                session["token"] = "None"
                token = session["token"]

            if token == "None":
                print("------- token none -------------")
                return jsonify({"success": False, "error": "Please login the system.. 0000"}), 401

            try:
                if jwt.decode(token, "ecommerce-secret"):
                    data = jwt.decode(token, "ecommerce-secret")

                    print("data --> ", data)

                    current_user = User.get_user_by_id(id=data["id"])
                    print("id: ", current_user.id, "\nusername: ", current_user.username)

                if current_user == None:
                    print("jjjjjjjjjjjjjjjj")
                    return jsonify({"success": False, "error": "Please login the system.. 1111"}), 401
            except Exception as e:
                print("ERROR IN LOGIN_REQUIRED 000 : ", e)
                return jsonify(
                        {
                            "success": False,
                            "error": "Signature has expired, please login the system..",
                        }
                    ), 401

            
            return f(current_user, *args, **kwargs)
        except Exception as e:
            print("ERROR IN LOGIN_REQUIRED 11111 : ", e)

            return jsonify({"success": False, "error": "Please login the system.. 2222"}), 401

    return decorator
