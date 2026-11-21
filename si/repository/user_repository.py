from sqlalchemy.orm import Session
from si.models.user import User

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_by_id(self, user_id: int) -> User | None:
        return self.db_session.query(User).filter(User.id == user_id).first()
