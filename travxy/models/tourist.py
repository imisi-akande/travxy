from travxy.db import db
from enum import Enum
import json

class GenderChoices(Enum):
    MALE = "Male"
    FEMALE = "Female"
    NEUTRAL = "Neutral"

class TouristInfoModel(db.Model):
    __tablename__ = 'tourists'
    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.Enum(GenderChoices,
                       values_callable=lambda x: [str(member.value) for member in GenderChoices]),
                       nullable=False,
                       default=GenderChoices.NEUTRAL.value,
                       server_default=GenderChoices.NEUTRAL.value)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    user = db.relationship("UserModel", back_populates="tourist")

    def __init__(self, nationality, gender, user_id):
        self.nationality = nationality
        self.gender = gender
        self.user_id = user_id

    def get_from_db(self):
        return {'nationality': self.nationality, 'gender':self.gender.value, 'user_id': self.user_id}

    def to_json(self):
        return {'nationality': self.nationality, 'gender':self.gender, 'user_id': self.user_id}


    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

