import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import Blueprint, jsonify, request, current_app, abort
from app.extensions import db
from app.models import Recurso, User
from app.schemas import RecursoSchema, UserLoginSchema
from marshmallow import ValidationError

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
recurso_schema = RecursoSchema()

# Decorador de protección JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
        if not token:
            abort(401, description="Se requiere un token de autenticación válido")

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # CAMBIO AQUÍ: Se reemplaza User.query.get(...) por db.session.get(User, ...)
            current_user = db.session.get(User, payload['user_id'])
            
            if not current_user:
                abort(401, description="Usuario no válido")
        except jwt.ExpiredSignatureError:
            abort(401, description="El token ha expirado")
        except jwt.InvalidTokenError:
            abort(401, description="Token inválido")

        return f(current_user, *args, **kwargs)
    return decorated

# AUTH: Registro
@api_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    if not data.get("username") or not data.get("password"):
        abort(400, description="Usuario y contraseña obligatorios")

    if User.query.filter_by(username=data["username"]).first():
        abort(400, description="El nombre de usuario ya existe")

    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"success": True, "message": "Usuario registrado exitosamente"}), 201

# AUTH: Login (Generación JWT)
@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not user.check_password(data.get("password", "")):
        abort(401, description="Credenciales inválidas")

    payload = {
        "user_id": user.id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"success": True, "token": token}), 200

# RUTAS DE RECURSOS (PROTEGIDAS)
@api_bp.route('/resources', methods=['GET'])
@token_required
def get_all_resources(current_user):
    recursos = Recurso.query.all()
    return jsonify({"success": True, "data": [r.to_dict() for r in recursos]}), 200

@api_bp.route('/resources', methods=['POST'])
@token_required
def create_resource(current_user):
    data = request.get_json(silent=True) or {}
    
    # Validación mediante Marshmallow Schema
    try:
        validated_data = recurso_schema.load(data)
    except ValidationError as err:
        abort(400, description=err.messages)

    nuevo_recurso = Recurso(
        nombre=validated_data["nombre"],
        descripcion=validated_data.get("descripcion", ""),
        estado=validated_data.get("estado", "activo")
    )
    db.session.add(nuevo_recurso)
    db.session.commit()
    
    return jsonify({"success": True, "data": nuevo_recurso.to_dict()}), 201