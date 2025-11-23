# backend/services/user_service.py
from backend.db.crud_users import create_user, get_user_by_username, update_user_language, update_profile

def onboard_user(username: str, phone: str = None, gender: str = None, language: str = "en-NG"):
    user = get_user_by_username(username)
    if user:
        return user
    return create_user(username=username, phone=phone, gender=gender, language=language)

def set_language(user_id: int, language: str):
    return update_user_language(user_id, language)
