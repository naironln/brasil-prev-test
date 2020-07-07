from flask import Flask, request
from flask_restplus import Api, Resource, fields
import json

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="Cool t-shirt store",
          description="Manage store products" )

logged_in = False

users_name_space = app.namespace('Users', description='Main API')

user_model = app.model("User Model",
                  {'name': fields.String(required=True,
                                         description="user's name",
                                         help="Name cannot be blank."),
                   'email': fields.String(required=True,
                                         description="user's email",
                                         help="email cannot be blank."),
                   'password': fields.String(required=True,
                                         description="user's password",
                                         help="email cannot be blank.")})
login_model = app.model("Login Model",
                   {'email': fields.String(required=True,
                                         description="user's email",
                                         help="email cannot be blank."),
                   'password': fields.String(required=True,
                                         description="user's password",
                                         help="email cannot be blank.")})

users_list = {}

@users_name_space.route("/")
class Users(Resource):

    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={ 'id': 'Specify the user id' })
    
    def get(self, id):
        try:
            user = users_list[id]
            return {
                "status": "User retrived",
                "name": user['name'],
                "email": user['email']
            }

        except KeyError as e:
            users_name_space.abort(500, e.__doc__, status="Unable to retrieve", statusCode="500")
        
        except Exception as e:
            users_name_space.abort(400, e.__doc__, status="Unable to retrieve", statusCode="400")

    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(user_model)      
    def post(self):
        try:
            email = request.json.get('email')
            users_list[email] = request.json

            return {
                "status": "New user registered",
                "name": users_list.get(email).get(email)
            }

        except KeyError as e:
            print(e)
            users_name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        
        except Exception as e:
            print(e)
            users_name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")
    

@users_name_space.route("/login")
class Login(Resource):

    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 401: 'unabble to authenticate' })
    @app.expect(login_model)      
    def post(self):
        try:
            email = request.json.get('email')
            user = users_list.get(email)

            if user['password'] != request.json.get('password'):
                raise KeyError
            
            logged_in = True
            return {
                "status": "Loged in"
            }

    
        except KeyError as e:
            print(e)
            users_name_space.abort(401, e.__doc__, status = "unabble to authenticate", statusCode = "401")
        
        except Exception as e:
            print(e)
            users_name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")




# products_name_space = app.namespace('Products', description='Main API')

# model = app.model("T-shirt Model",
#                   {'name': fields.String(required=True,
#                                          description="Name of the user",
#                                          help="Name cannot be blank.")})

# users_list = {}

# @products_name_space.route("/<int:id>")
# class Product(Resource):

#     @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
#              params={ 'id': 'Specify the user id' })
    
#     def get(self, id):
#         try:
#             user = users_list[id]
#             return {
#                 "status": "User retrived",
#                 "name": user
#             }
#         except KeyError as e:
#             products_name_space.abort(500, e.__doc__, status="Unable to retrieve", statusCode="500")
        
#         except Exception as e:
#             products_name_space.abort(400, e.__doc__, status="Unable to retrieve", statusCode="400")

#     @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
#              params={ 'id': 'Specify the user id' })
             
#     @app.expect(model)      
#     def post(self, id):
#         try:
#             users_list[id] = request.json['name']
#             return {
#                 "status": "New user registered",
#                 "name": users_list[id]
#             }

#         except KeyError as e:
#             print(e)
#             products_name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        
#         except Exception as e:
#             print(e)
#             products_name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")