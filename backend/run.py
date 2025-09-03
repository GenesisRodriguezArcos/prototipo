from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from sqlalchemy import Sequence

app = Flask(__name__)

# =========================
# CONFIGURAR SQLAlchemy
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Configurar CORS (permite todos los orígenes)
CORS(app, resources={r"/*": {"origins": "*"}})

db = SQLAlchemy(app)

# =========================
# MODELO DE BASE DE DATOS
# =========================
class Producto(db.Model):
    __tablename__ = 'PRODUCTOS'
    id = db.Column(db.Integer, Sequence('productos_seq'), primary_key=True)  # 👈 con secuencia
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock
        }

# Crear tabla si no existe
with app.app_context():
    db.create_all()

# =========================
# RUTAS
# =========================

# 🌐 Ruta base
@app.route("/")
def home():
    return jsonify({"mensaje": "✅ Servidor Flask funcionando con Oracle - Productos"}), 200

# 🔄 Crear producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()

    if not data.get('nombre') or not data.get('precio') or not data.get('stock'):
        return jsonify({'error': 'Faltan campos obligatorios: nombre, precio, stock'}), 400

    producto = Producto(**data)
    db.session.add(producto)
    db.session.commit()
    return jsonify({'mensaje': 'Producto creado', 'producto': producto.to_dict()}), 201

# 📋 Listar todos los productos
@app.route('/productos', methods=['GET'])
def listar_productos():
    todos = Producto.query.all()
    return jsonify([p.to_dict() for p in todos]), 200

# 🔎 Obtener producto por ID
@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify(producto.to_dict()), 200

# 📝 Modificar producto por ID
@app.route('/productos/<int:id>', methods=['PUT'])
def modificar_producto(id):
    data = request.get_json()
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    for key, value in data.items():
        if hasattr(producto, key):
            setattr(producto, key, value)

    db.session.commit()
    return jsonify({'mensaje': 'Producto actualizado', 'producto': producto.to_dict()}), 200

# 🗑️ Eliminar producto por ID
@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    db.session.delete(producto)
    db.session.commit()
    return jsonify({'mensaje': 'Producto eliminado'}), 200

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
