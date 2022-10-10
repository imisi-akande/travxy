from travxy.db import db

class ApplicationExperienceModel(db.Model):
    __tablename__ = 'app_experience'
    id = db.Column(db.Integer, primary_key=True)
    tourist_id = db.Column(db.Integer, db.ForeignKey('tourists.id',
                                                    ondelete="CASCADE"))
    tourist = db.relationship('TouristInfoModel', back_populates="app_experiences")
    comment = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()


    def json(self):
        return {'tourist_id': self.tourist_id, 'comment': self.comment,
                'rating':self.rating}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()