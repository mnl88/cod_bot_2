import sqlalchemy as sa
from utils.db_api import TimedBaseModel


class Platform(TimedBaseModel):
    __tablename__ = 'text_platforms'
    # __tablename__ = 'platforms'

    id = sa.Column(sa.Integer, primary_key=True)  # ID
    name = sa.Column(sa.String(100), unique=True)  # (PS4, PS5, PS4 Pro)
    description = sa.Column('description', sa.String(500))  # Personal Computer/Playstation 4/Xbox Series X
    # device_type = sa.Column(sa.Integer, sa.ForeignKey('test_platform_types.id'), nullable=True)  # (PC, PS, Xbox)
    # device_type = sa.Column(sa.Integer, sa.ForeignKey('platform_types.id'), nullable=True)  # (PC, PS, Xbox)

