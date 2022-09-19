from travxy.db import db
from ..models import bcrypt

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    isactive = db.Column(db.Boolean, default=True, nullable=False)
    tourist = db.relationship("TouristInfoModel", back_populates="user",
                                uselist=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
                'id': self.id,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'username': self.username,
                'email': self.email,
                'isactive': self.isactive
                }
    def username_json(self):
        return {
                'user_id':self.id,
                'last_name': self.last_name,
                'first_name': self.first_name,
                'username': self.username,
                }

    def for_admin_with_tourist_json(self):
        return {**self.json(),
                    'tourist_status': self.tourist.json_with_tourist_status()}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @staticmethod
    def generate_hash(password):
        return bcrypt.generate_password_hash(password,
                                            rounds=10).decode("utf-8")
