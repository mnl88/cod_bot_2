import sqlalchemy as sa
from utils.db_api import TimedBaseModel


class TG_Account(TimedBaseModel):
    __tablename__ = 'test_tg_accounts'
    # __tablename__ = 'tg_accounts'

    id = sa.Column(sa.Integer, primary_key=True)
    username: sa.Column = sa.Column(sa.String(100))
    # person_id = sa.Column(sa.Integer, sa.ForeignKey('persons.id'), nullable=False)
    person_id = sa.Column(sa.Integer, sa.ForeignKey('test_persons.id'), nullable=False)
    is_bot = sa.Column('is_bot', sa.Boolean, default=False)
    first_name = sa.Column('first_name', sa.String(100))
    language_code = sa.Column('language_code', sa.String(50))

    def __repr__(self):
        return "<TG_Account: (id: '%s', username: '%s', first_name: '%s')>" % (self.id, self.username, self.first_name)

