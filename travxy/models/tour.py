from travxy.db import db

class TourModel(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(80), nullable=False)
    about = db.Column(db.String(500), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"))
    category = db.relationship('CategoryModel', back_populates="tours")
    
    def __init__(self, name, location, about, category_id):
        self.name = name
        self.location = location
        self.about = about
        self.category_id = category_id

    def json(self):
        return{'name': self.name, 'location': self.location, 'about': self.about, 'category_id': self.category_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


