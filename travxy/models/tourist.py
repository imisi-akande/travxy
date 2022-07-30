from travxy.db import db

from sqlalchemy.dialects.postgresql import ENUM

from travxy.models.detail import tourist_detail

class TouristInfoModel(db.Model):
    __tablename__ = 'tourists'
    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(80), nullable=False)
    gender = db.Column(ENUM("Male", "Female", "Neutral",
                                       name="gender_level", create_type=False))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    user = db.relationship("UserModel", back_populates="tourist")
    tour_details_of_tourists = db.relationship(
            "DetailModel", secondary=tourist_detail, back_populates="tourists_tour_details",
            lazy='dynamic', cascade="all, delete")

    def __init__(self, nationality, gender, user_id):
        self.nationality = nationality
        self.gender = gender
        self.user_id = user_id

    def json(self):
        return {'nationality': self.nationality, 'gender':self.gender, 'user_id': self.user_id, 'tour_details':[tour_details.json() for tour_details in self.tour_details_of_tourists.all()]}

    @classmethod
    def find_by_name(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_user(cls, current_identity):
        return cls.query.filter_by(user_id=current_identity).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

