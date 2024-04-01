from marshmallow import Schema, fields, validate


# Schema do Marshmallow para validar e serializar dados de usuário
class UserSchema(Schema):
    """Esquema para validar dados de usuário."""
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()

class UserSchemaView(Schema):
    """Esquema para serializar dados de usuário."""
    id = fields.Str()
    username = fields.Str()
    email = fields.Email()

class UserLoginSchema(Schema):
    """Esquema para serializar dados de usuário."""
    username = fields.Str()
    password = fields.Str()


class AdditionalClaimsSchema(Schema):
    """Schema para os campos 'user_id' e 'username' na resposta."""
    user_id = fields.Int(required=True)
    username = fields.Str(required=True)

class UserAuthenticatedSchema(Schema):
    """Schema para a resposta completa, incluindo 'access_token' e 'additional_claims'."""
    access_token = fields.Str(required=True)
    additional_claims = fields.Nested(AdditionalClaimsSchema, required=True)


class LogoutOutputSchema(Schema):
    """Schema de saída para a rota de logout."""
    message = fields.Str(required=True, description="Mensagem indicando que o logout foi bem-sucedido.")
    user_id = fields.Int(required=True, description="ID do usuário que fez logout.")
    
