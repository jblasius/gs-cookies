from app import app, db, DDL, event


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True, unique=True)
    last_seen = db.Column(db.DateTime)
    social_id = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):  # pragma: no cover
        return '<User %r>' % (self.user_name)


class UserGirl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True)
    girl_name = db.Column(db.String(64), index=True)


class Girl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    girl_name = db.Column(db.String(64), index=True)
    avatar = db.String(db.String(255))

    def __repr__(self):  # pragma: no cover
        return '<User %r>' % (self.girl_name)


class AsyncOperationStatus(db.Model):
    __tablename__ = 'async_operation_status'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column('code', db.String(20), nullable=True)


class AsyncOperation(db.Model):
    __tablename__ = 'async_operation'
    id = db.Column(db.Integer, primary_key=True)
    async_operation_status_id = db.Column(db.Integer, db.ForeignKey(AsyncOperationStatus.id))
    user_profile_id = db.Column(db.Integer, db.ForeignKey(User.id))

    status = db.relationship('AsyncOperationStatus', foreign_keys=async_operation_status_id)
    user_profile = db.relationship('User', foreign_keys=user_profile_id)


event.listen(
    AsyncOperationStatus.__table__, 'after_create',
    DDL(
        """ INSERT INTO async_operation_status (id,code) VALUES(1,'pending'),
        (2, 'ok'),(3, 'error'); """)
    )

