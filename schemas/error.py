from marshmallow import Schema, fields

class ErrorSchema(Schema):
    """ Define como uma mensagem de erro será representada
    """
    message = fields.Str(required=True)