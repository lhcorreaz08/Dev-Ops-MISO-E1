from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dotenv import load_dotenv
from os import getenv
from modelos import db
from vistas import VistaBlacklist


def set_env():
    load_dotenv()
    global DATABASE_URL
    DATABASE_URL = getenv("DATABASE_URL")
    global JWT_SECRET_KEY
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")

set_env()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
#api.add_resource(VistaOferta, '/offers')
#api.add_resource(VistaOfertaById, '/offers/<id>')
#api.add_resource(Health, '/offers/ping')


#if __name__ == "__main__":
#    port = int(os.environ.get('PORT', 4001))
#    app.run(debug=True, host='0.0.0.0', port=port)        
if __name__ == '__main__':
    app.run(debug=True)

