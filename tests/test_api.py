def test_unauthorized_access(client):
    """Verifica que el acceso sin token devuelva 401"""
    response = client.get("/api/v1/resources")
    assert response.status_code == 401
    assert response.get_json()["success"] is False

def test_login_success(client):
    """Verifica la obtención correcta del JWT"""
    response = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()

def test_create_resource_valid(client, auth_header):
    """Verifica la creación de un recurso pasando validación"""
    response = client.post(
        "/api/v1/resources",
        json={"nombre": "Recurso de prueba", "descripcion": "Testing automatizado"},
        headers=auth_header
    )
    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["nombre"] == "Recurso de prueba"

def test_create_resource_invalid_schema(client, auth_header):
    """Verifica el rechazo de Marshmallow ante datos inválidos"""
    response = client.post(
        "/api/v1/resources",
        json={"descripcion": "Sin nombre requerido"},
        headers=auth_header
    )
    assert response.status_code == 400
    assert response.get_json()["success"] is False