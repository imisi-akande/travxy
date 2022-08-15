from travxy.db import db

from sqlalchemy.dialects.postgresql import ENUM

from travxy.models.detail import tourist_detail

class TouristInfoModel(db.Model):
    __tablename__ = 'tourists'
    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(80), nullable=False)
    gender = db.Column(ENUM("Male", "Female", "Neutral",
                                       name="gender_level", nullable=False,
                                       create_type=False))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    user = db.relationship("UserModel", back_populates="tourist")
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"))
    role = db.relationship("RoleModel", back_populates = "tourists")


    tour_details_of_tourists = db.relationship(
            "DetailModel", secondary=tourist_detail, back_populates="tourists_info",
            lazy='dynamic', cascade="all, delete")

    details_info = db.relationship(
            "DetailModel", secondary=tourist_detail, viewonly=True)

    def json(self):
        return {'tourist_id': self.id, 'nationality': self.nationality,
                'gender': self.gender}

    def with_details_json(self):
        return {**self.json(), 'tour_details':[tour_details.json() for tour_details in self.details_info]}

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

