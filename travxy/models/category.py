from travxy.db import db

class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    tours = db.relationship('TourModel', back_populates='category', lazy='dynamic')

    def json(self):
        return {'id': self.id, 'name': self.name}

    def with_tour_json(self):
        return {'id': self.id, 'name': self.name, 'tours': [tour.json() for tour in self.tours.all()]}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


