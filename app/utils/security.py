from flask_jwt_extended import create_access_token, get_jwt
import datetime
import time

def crear_token_usuario(usuario):
    """Crea un token JWT con la estructura exacta que necesitas"""
    
    # Calcular timestamps
    now = datetime.datetime.utcnow()
    nbf_timestamp = int(time.mktime(now.timetuple()))  # Not Before
    exp_timestamp = int(time.mktime((now + datetime.timedelta(hours=24)).timetuple()))  # Expiration
    
    # Configurar claims personalizados
    additional_claims = {
        'id': usuario.id,
        'username': usuario.username,
        'nbf': nbf_timestamp,
        'exp': exp_timestamp
    }
    
    token = create_access_token(
        identity=usuario.username,  # O puedes usar usuario.id
        additional_claims=additional_claims
    )
    return token
