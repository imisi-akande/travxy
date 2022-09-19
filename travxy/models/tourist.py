from travxy.db import db

from sqlalchemy import Enum

from travxy.models.detail import tourist_detail

class TouristInfoModel(db.Model):
    __tablename__ = 'tourists'
    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(80), nullable=False)
    gender = db.Column(Enum("Male", "Female", "Neutral",
                                       name="gender_level", nullable=False))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", 
                        ondelete="CASCADE"))
    user = db.relationship("UserModel", back_populates="tourist")
    

    place_details_of_tourists = db.relationship(
            "DetailModel", secondary=tourist_detail,
            back_populates="tourists_info",
            lazy='dynamic', cascade="all, delete")

    details_info = db.relationship(
            "DetailModel", secondary=tourist_detail, viewonly=True)

    def json(self):
        return {'tourist_id': self.id, 'nationality': self.nationality,
                'gender': self.gender}

    def from_admin_json(self):
        return {'tourist_id': self.id, 'nationality': self.nationality,
                'gender': self.gender}

    def json_with_user_name(self):
        return {**self.json(), 'user_detail': self.user.username_json()}

    def json_with_user_detail(self):
        return {**self.json(), 'user_detail': self.user.json()}

    def json_with_tourist_status(self):
        return {'nationality': self.nationality,
                'gender': self.gender}

    # def json_with_role(self):
    #     return {**self.json_with_user_detail(), 'role_id': self.role_id}

    def with_details_json(self):
        return {**self.json(), 'place_details':[place_details.json()
                    for place_details in self.details_info]}

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

