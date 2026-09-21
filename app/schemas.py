from marshmallow import Schema, fields, validate

class RecursoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    descripcion = fields.Str(validate=validate.Length(max=255))
    estado = fields.Str(validate=validate.OneOf(["activo", "inactivo"]))
    creado_en = fields.DateTime(dump_only=True)

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)