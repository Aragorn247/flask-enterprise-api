import pytest
from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "esta_es_una_clave_secreta_super_segura_de_mas_de_32_caracteres_12345"
    })

    with app.app_context():
        db.create_all()
        # Crear usuario por defecto para pruebas
        user = User(username="testuser")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_header(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    token = response.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}