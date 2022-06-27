from db import db

class TourModel(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(80))
    about = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories_id'))
    category = db.relationship('CategoryModel')

    def __init__(self, name, location, about, category_id):
        self.name = name
        self.location = location
        self.about = about
        self.category_id = category_id

    def json(self):
        return{'name': self.name, 'location': self.location, 'about': self.about}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit(self)


