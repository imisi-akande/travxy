from travxy.db import db


tourist_detail = db.Table('tourist_detail',
                       db.Column('tourist_id', db.Integer, db.ForeignKey('tourists.id'), primary_key=True),
                       db.Column('detail_id', db.Integer, db.ForeignKey('details.id'), primary_key=True)
                    )
class DetailModel(db.Model):
    __tablename__ = 'details'

    id = db.Column(db.Integer, primary_key=True)
    tour_name = db.Column(db.String(80), nullable=False)
    departure = db.Column(db.String(80), nullable=False)
    transportation = db.Column(db.String(80), nullable=False)
    experience = db.Column(db.Text, nullable=False)
    upvote = db.Column(db.Integer, nullable=False)
    estimated_cost = db.Column(db.Float, nullable=False)
    tourists_tour_details = db.relationship(
        "TouristInfoModel", secondary=tourist_detail, back_populates="tour_details_of_tourists",
        lazy='dynamic'
        )
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"))
    category = db.relationship('CategoryModel', back_populates="details")

    def __init__(self, tour_name, departure, transportation, experience, upvote, estimated_cost, category_id):
        self.tour_name = tour_name
        self.departure = departure
        self.transportation = transportation
        self.experience = experience
        self.upvote = upvote
        self.estimated_cost = estimated_cost
        self.category_id = category_id

    def json(self):
        return {'detail_id': self.id, 'tour_name': self.tour_name, 'departure': self.departure, 'transportation': self.transportation,
                'experience': self.experience, 'upvote': self.upvote,
                'estimated_cost': self.estimated_cost, 'category': self.category_id}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(tour_name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



