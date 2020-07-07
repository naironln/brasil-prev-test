from flask import Flask, request
from flask_restplus import Api, Resource, fields

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="Cool t-shirt store",
          description="Manage store products" )

name_space = app.namespace('Users', description='Main API')

model = app.model("User Model",
                  {'name': fields.String(required=True,
                                         description="Name of the user",
                                         help="Name cannot be blank.")})

users_list = {}

@name_space.route("/<int:id>")
class MainClass(Resource):

    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={ 'id': 'Specify the user id' })
    
    def get(self, id):
        try:
            user = users_list[id]
            return {
                "status": "User retrived",
                "name": user
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Unable to retrieve", statusCode="500")
        
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Unable to retrieve", statusCode="400")

    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
             params={ 'id': 'Specify the user id' })
             
    @app.expect(model)      
    def post(self, id):
        try:
            users_list[id] = request.json['name']
            return {
                "status": "New user registered",
                "name": users_list[id]
            }

        except KeyError as e:
            print(e)
            name_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
        
        except Exception as e:
            print(e)
            name_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")