from travxy.db import db
from sqlalchemy.dialects.postgresql import ENUM


tourist_detail = db.Table('tourist_detail',
                       db.Column('tourist_id', db.Integer, db.ForeignKey('tourists.id'), primary_key=True),
                       db.Column('detail_id', db.Integer, db.ForeignKey('details.id'), primary_key=True)
                    )
class DetailModel(db.Model):
    __tablename__ = 'details'

    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(80), nullable=False)
    transportation = db.Column(ENUM("Air", "Road", "Rail", "Water",
                                       name="transportation_types", nullable=False, create_type=False))
    travel_buddies_created_by = db.Column(db.Integer, db.ForeignKey('tourists.id', ondelete="CASCADE"))
    estimated_cost = db.Column(db.Numeric(precision=10, asdecimal=False, decimal_return_scale=None), nullable=False)
    tourists_info = db.relationship(
        "TouristInfoModel", secondary=tourist_detail, back_populates="tour_details_of_tourists",
        lazy='dynamic'
        )
    tourists = db.relationship(
        "TouristInfoModel", secondary=tourist_detail, viewonly=True
        )
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id', ondelete="CASCADE"))
    tour = db.relationship('TourModel', back_populates="details")

    def json(self):
        return {'detail_id': self.id, 'tour_id': self.tour_id,
                'departure': self.departure,
                'transportation': self.transportation,
                'estimated_cost': self.estimated_cost,
                'created_by': self.travel_buddies_created_by
                }


    def with_tourist_json(self):
        return {**self.json(), 'tourists': [tourist.json() for tourist in self.tourists]}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_tour_id(cls, id):
        return cls.query.filter_by(tour_id=id).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
