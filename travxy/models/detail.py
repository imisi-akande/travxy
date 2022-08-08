from travxy.db import db


tourist_detail = db.Table('tourist_detail',
                       db.Column('tourist_id', db.Integer, db.ForeignKey('tourists.id'), primary_key=True),
                       db.Column('detail_id', db.Integer, db.ForeignKey('details.id'), primary_key=True)
                    )
class DetailModel(db.Model):
    __tablename__ = 'details'

    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(80), nullable=False)
    transportation = db.Column(db.String(80), nullable=False)
    travel_buddy_one = db.Column(db.Integer, nullable=True)
    travel_buddy_two = db.Column(db.Integer, nullable=True)
    travel_buddy_three = db.Column(db.Integer, nullable=True)

    experience = db.Column(db.Text, nullable=False)
    upvote = db.Column(db.Integer, nullable=False)
    estimated_cost = db.Column(db.Float, nullable=False)
    tourists_info = db.relationship(
        "TouristInfoModel", secondary=tourist_detail, back_populates="tour_details_of_tourists",
        lazy='dynamic'
        )
    tourists = db.relationship(
        "TouristInfoModel", secondary=tourist_detail, viewonly=True
        )
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id', ondelete="CASCADE"))
    tour = db.relationship('TourModel', back_populates="details")

    def __init__(self, tour_id, tour_name, departure, transportation, travel_buddy_one, travel_buddy_two, travel_buddy_three, experience, upvote, estimated_cost, category_id):
        self.tour_id = tour_id
        self.tour_name = tour_name
        self.departure = departure
        self.transportation = transportation
        self.travel_buddy_one = travel_buddy_one
        self.travel_buddy_two = travel_buddy_two
        self.travel_buddy_three = travel_buddy_three

        self.experience = experience
        self.upvote = upvote
        self.estimated_cost = estimated_cost
        self.category_id = category_id

    def json(self):
        return {'detail_id': self.id, 'tour_id': self.tour_id, 
                'departure': self.departure,
                'travel_buddy_one': self.travel_buddy_one, 
                'travel_buddy_two': self.travel_buddy_two, 
                'travel_buddy_three': self.travel_buddy_three, 
                'transportation': self.transportation,
                'experience': self.experience, 'upvote': self.upvote,
                'estimated_cost': self.estimated_cost}

    def with_tourist_json(self):
        return {**self.json(), 'tourists': [tourist.json() for tourist in self.tourists]}

    def with_tourist_info_json(self):
        return {**self.json(), 'tourists': [tourist.json() for tourist in self.tourists_info]}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(tour_id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



