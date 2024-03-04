from api.db.database import get_db
from api.models.refresh_token import RefreshToken
from api.models.user import User


async def sotre_refresh_to_db(token, username):
    db = next(get_db())
    user_id = db.query(User.id).filter(User.username == username).first()
    db.merge(RefreshToken(user_id=user_id, token=token))
