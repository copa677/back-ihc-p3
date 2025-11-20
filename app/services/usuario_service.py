from app.models.usuario import Usuario
from app import db
from sqlalchemy.exc import SQLAlchemyError

class UsuarioService:
    
    @staticmethod
    def crear_usuario(username, password, tipo_usuario='usuario'):
        """Crea un nuevo usuario"""
        try:
            # Verificar si el usuario ya existe
            if Usuario.query.filter_by(username=username).first():
                return None, "El nombre de usuario ya existe"
            
            usuario = Usuario(
                username=username,
                tipo_usuario=tipo_usuario
            )
            usuario.set_password(password)
            
            db.session.add(usuario)
            db.session.commit()
            
            return usuario, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error en la base de datos: {str(e)}"
    
    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        """Obtiene un usuario por su ID"""
        try:
            return Usuario.query.get(usuario_id)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_usuario_por_username(username):
        """Obtiene un usuario por su username"""
        try:
            return Usuario.query.filter_by(username=username).first()
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def autenticar_usuario(username, password):
        """Autentica un usuario con username y password"""
        try:
            usuario = Usuario.query.filter_by(username=username, esta_activo=True).first()
            if usuario and usuario.check_password(password):
                return usuario, None
            return None, "Credenciales inválidas"
        except SQLAlchemyError:
            return None, "Error en la autenticación"
    
    @staticmethod
    def obtener_todos_los_usuarios():
        """Obtiene todos los usuarios"""
        try:
            return Usuario.query.all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def actualizar_usuario(usuario_id, datos_actualizados):
        """Actualiza los datos de un usuario"""
        try:
            usuario = Usuario.query.get(usuario_id)
            if not usuario:
                return None, "Usuario no encontrado"
            
            if 'username' in datos_actualizados:
                usuario.username = datos_actualizados['username']
            if 'tipo_usuario' in datos_actualizados:
                usuario.tipo_usuario = datos_actualizados['tipo_usuario']
            if 'password' in datos_actualizados:
                usuario.set_password(datos_actualizados['password'])
            
            db.session.commit()
            return usuario, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar usuario: {str(e)}"
    
    @staticmethod
    def eliminar_usuario(usuario_id):
        """Elimina un usuario (borrado lógico)"""
        try:
            usuario = Usuario.query.get(usuario_id)
            if not usuario:
                return False, "Usuario no encontrado"
            
            usuario.esta_activo = False
            db.session.commit()
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar usuario: {str(e)}"