from travxy.db import db
from sqlalchemy.sql import func

class TouristExperienceModel(db.Model):
    __tablename__ = 'tourist_experience'
    tourist_id = db.Column(db.Integer, primary_key=True)
    detail_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


    def json(self):
        return {'tourist_id': self.tourist_id, 'detail_id': self.detail_id,
                'comment': self.comment, 'rating': self.rating,
                'duration': self.duration,
                'time_created': str(self.time_created)
                }

    def with_time_updated_json(self):
        return {'tourist_id': self.tourist_id, 'detail_id': self.detail_id,
                'comment': self.comment, 'rating': self.rating,
                'duration': self.duration,
                'time_created': str(self.time_created),
                'time_updated': str(self.time_updated)}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
