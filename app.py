from flask import Flask, request
from flask_restplus import Api, Resource, fields
import json

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="Cool t-shirt store",
          description="Manage store products" )


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

    # @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
    #          params={ 'id': 'Specify the user id' })
    
    # def get(self, id):
    #     try:
    #         user = users_list[id]
    #         return {
    #             "status": "User retrived",
    #             "name": user['name'],
    #             "email": user['email']
    #         }

    #     except KeyError as e:
    #         users_name_space.abort(500, e.__doc__, status="Unable to retrieve", statusCode="500")
        
    #     except Exception as e:
    #         users_name_space.abort(400, e.__doc__, status="Unable to retrieve", statusCode="400")

    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(user_model)      
    def post(self):
        try:
            email = request.json.get('email')
            users_list[email] = request.json

            return {
                "status": "New user registered",
                "user": users_list.get(email)['email']
            }

        except KeyError as e:
            users_name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        
        except Exception as e:
            users_name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")
    

LOGGED_IN = False
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
            LOGGED_IN = True
            return {
                "status": "Loged in"
            }

    
        except KeyError as e:
            users_name_space.abort(401, e.__doc__, status = "unabble to authenticate", statusCode = "401")
        
        except Exception as e:
            users_name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")




products_name_space = app.namespace('Products', description='Main API')

product_model = app.model("T-shirt Model",
                          {'name': fields.String(required=True,
                                                 description="Name of the product",
                                                 help="Name cannot be blank."),
                           'color': fields.String(required=True,
                                                 description="Color of the product",
                                                 help="Color cannot be blank."),
                           'id': fields.Integer(required=True,
                                                 description="Id of the product",
                                                 help="Id cannot be blank.")})

order_model = app.model("Order Model",
                        {"id": fields.Integer(required=True,
                                              description="Id of the product to be oredered",
                                              help="id cannot be blank")})

products_list = {'0': {'name': 'red cool t-shirt', 'color': 'red'},
                 '1': {'name': 'blue and yellow lame t-shirt', 'color': 'blue and yellow'},}

@products_name_space.route("/")
class Products(Resource):
    
    def get(self):
        try:
            return {
                "status": "User retrived",
                "name": products_list
            }
        except KeyError as e:
            products_name_space.abort(500, e.__doc__, status="Unable to retrieve", statusCode="500")
        
        except Exception as e:
            products_name_space.abort(400, e.__doc__, status="Unable to retrieve", statusCode="400")

             
    @app.expect(product_model)      
    def post(self):
        try:
            product = request.json
            print(product)

            if product['id'] in products_list:
                return {
                    "status": "cannot register new product",
                    "message": "product's id is already in use"
                }

            users_list[product['id']] = product
            return {
                "status": "New product registered",
                "product": product
            }

        except KeyError as e:
            products_name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        
        except Exception as e:
            products_name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")


@products_name_space.route("/place_order")
class PlaceOrder(Resource):
    @app.expect(order_model)      
    def post(self):
        try:

            product = products_list.get(request.json.get('id'))
            return {
                "status": "Order placed",
                "product": product
            }

        except KeyError as e:
            products_name_space.abort(401, e.__doc__, status = "Unauthorized", statusCode = "401")
        
        except Exception as e:
            products_name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")
