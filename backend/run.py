from flask import Flask, request, jsonify
from flask_sqlalchemy import flask_sqlalchemy
from flask_cors import CORS
from config import SQALCHEMY_DATABASE_URI
app = Flask(__name__)
#configuración con cors
CORS(app, recurse=(r"/*":{"origins":"*"}))

app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db = SQLAlchemy(app) 

#Definir la base de datos 
class Productos(db.Model):
    __tablename__= 'productos'
    id = db.column(db.Integer,primary_key=tru)
    nombre = db.column(db.String.(100),nullable=False)
    precio = db.column(db.Float..nullable=False)
    def to_dict(self)
    return{
        'id': self.id,
        'now,bre': self.nombre,
        'precio': self.precio,
    }
    #Crear las
    With 