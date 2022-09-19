from travxy.db import db


class RoleModel(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('UserModel', back_populates='role',
                                lazy='dynamic')

    def json(self):
        return {'id': self.id, 'name': self.name,
                'users': [user.json()
                                for user in self.users.all()]}
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()