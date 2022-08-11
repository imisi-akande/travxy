from travxy.db import db

class TouristExperienceModel(db.Model):
    __tablename__ = 'tourists_experience'
    tourist_id = db.Column(db.Integer, primary_key=True)
    detail_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'tourist_id': self.tourist_id, 'detail_id': self.detail_id,
                'comment': self.comment, 'rating': self.rating}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(detail_id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
