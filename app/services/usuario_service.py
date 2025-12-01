from app.models.user_delivery import UserDelivery
from app import db
from sqlalchemy.exc import SQLAlchemyError

class UsuarioService:
    
    @staticmethod
    def crear_usuario(username, password):
        """Crea un nuevo usuario"""
        try:
            # Verificar si el usuario ya existe
            if UserDelivery.query.filter_by(username=username).first():
                return None, "El nombre de usuario ya existe"
            
            usuario = UserDelivery(
                username=username,
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
            return UserDelivery.query.get(usuario_id)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_usuario_por_username(username):
        """Obtiene un usuario por su username"""
        try:
            return UserDelivery.query.filter_by(username=username).first()
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def autenticar_usuario(username, password):
        """Autentica un usuario con username y password"""
        try:
            usuario = UserDelivery.query.filter_by(username=username, esta_activo=True).first()
            if usuario and usuario.check_password(password):
                return usuario, None
            return None, "Credenciales inválidas"
        except SQLAlchemyError:
            return None, "Error en la autenticación"
    
    @staticmethod
    def obtener_todos_los_usuarios():
        """Obtiene todos los usuarios"""
        try:
            return UserDelivery.query.all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def actualizar_usuario(usuario_id, datos_actualizados):
        """Actualiza los datos de un usuario"""
        try:
            usuario = UserDelivery.query.get(usuario_id)
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
            usuario = UserDelivery.query.get(usuario_id)
            if not usuario:
                return False, "Usuario no encontrado"
            
            usuario.esta_activo = False
            db.session.commit()
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar usuario: {str(e)}"
        
    @staticmethod
    def actualizar_ubicacion_delivery(delivery_id, nueva_latitud, nueva_longitud):
        """
        Actualiza la ubicación de un delivery y retorna su id_orden actual.
        
        Args:
            delivery_id: ID del delivery
            nueva_latitud: Nueva latitud
            nueva_longitud: Nueva longitud
        
        Returns:
            Tuple (id_orden_actual, delivery_actualizado, error)
            - id_orden_actual: El id_orden actual del delivery (puede ser None)
            - delivery_actualizado: El objeto UserDelivery actualizado
            - error: Mensaje de error si ocurre
        """
        try:
            # Obtener el delivery
            delivery = UserDelivery.query.get(delivery_id)
            if not delivery:
                return None, None, "Delivery no encontrado"
            
            # Verificar que el delivery esté activo
            if not delivery.esta_activo:
                return delivery.id_orden, delivery, "Delivery inactivo (ubicación actualizada igualmente)"
            
            # Actualizar ubicación
            delivery.latitud = nueva_latitud
            delivery.longitud = nueva_longitud
            
            db.session.commit()
            
            # Retornar id_orden actual (puede ser None o un número)
            return delivery.id_orden, delivery, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, None, f"Error en la base de datos: {str(e)}"
        except Exception as e:
            return None, None, f"Error al actualizar ubicación: {str(e)}"