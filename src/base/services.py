from src.user.models import User


def get_path_upload_avatar(instanse: User, file):
    """Построение пути к файлу, format: (media)/avatar/user_id/photo.jpg"""
    return f"avatar/{instanse.id}/{file}"
