from travxy.db import db

tour_category = db.Table('tour_category',
                       db.Column('tour_id', db.Integer, db.ForeignKey('tours.id'), primary_key=True),
                       db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
                    )

class TourModel(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    about = db.Column(db.String(500), nullable=False)
    details = db.relationship('DetailModel', back_populates='tour',
                                lazy='dynamic')
    details_view = db.relationship('DetailModel', back_populates='tour',
                                viewonly=True)

    categories_info = db.relationship(
        "CategoryModel", secondary=tour_category,
        back_populates="tour_details",
        lazy='dynamic', cascade="all, delete")

    category = db.relationship(
        "CategoryModel", secondary=tour_category,
        back_populates="tour_details",
        viewonly=True)

    def json(self):
        return {'tour_id': self.id, 'name': self.name,
                'location': self.location, 'country': self.country,
                'about': self.about}

    def with_category_json(self):
        return {**self.json(), 'category': [category.json() for category in self.categories_info]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

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


