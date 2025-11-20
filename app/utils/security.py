from flask_jwt_extended import create_access_token


def crear_token_usuario(usuario):
    """Crea un token JWT para el usuario"""
    identity = {
        'id': usuario.id,
        'username': usuario.username,
        'tipo_usuario': usuario.tipo_usuario
    }
    
    token = create_access_token(
        identity=identity
    )
    return token

def extraer_datos_token(identity):
    """Extrae los datos del usuario del token JWT"""
    if isinstance(identity, dict):
        return {
            'id': identity.get('id'),
            'username': identity.get('username'),
            'tipo_usuario': identity.get('tipo_usuario')
        }
    # Si identity no es un diccionario, podría ser solo el ID
    return {
        'id': identity,
        'username': None,
        'tipo_usuario': None
    }