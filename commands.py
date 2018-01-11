from app import app
from models import User, db

def clear_users():
    with app.app_context():
        users = User.query.filter_by().delete()
        db.session.commit()

# clear_users()