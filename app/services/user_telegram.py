from app.models.user_telgram import UserTelegram
from app import db
from sqlalchemy.exc import SQLAlchemyError

class UserTelegramService:
    
    @staticmethod
    def create_user_telegram(chat_id):
        """
        Inserta un nuevo usuario de Telegram si no existe el chat_id
        Retorna el usuario y un booleano indicando si fue creado
        """
        # Verificar si ya existe el chat_id
        existing_user = UserTelegram.query.filter_by(chat_id=chat_id).first()
        
        if existing_user:
            return existing_user, False  # Ya existe, no se creó nuevo
        
        # Crear nuevo usuario
        new_user = UserTelegram(chat_id=chat_id)
        db.session.add(new_user)
        
        try:
            db.session.commit()
            return new_user, True
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_users():
        """Obtiene todos los usuarios de Telegram"""
        return UserTelegram.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        """Obtiene un usuario por ID"""
        return UserTelegram.query.get(user_id)

    @staticmethod
    def get_user_by_chat_id(chat_id):
        """Obtiene un usuario por chat_id"""
        return UserTelegram.query.filter_by(chat_id=chat_id).first()

    @staticmethod
    def delete_user(user_id):
        """Elimina un usuario por ID"""
        user = UserTelegram.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False