import sqlalchemy as sa
from utils.db_api import TimedBaseModel


class PlatformType(TimedBaseModel):
    __tablename__ = 'test_platform_types'
    # __tablename__ = 'platform_types'

    id = sa.Column(sa.Integer, primary_key=True)  # ID
    name = sa.Column(sa.String(100), unique=True)  # (PC, PS, Xbox)
    description = sa.Column('description', sa.String(500))  # Personal Computer/Playstation/Xbox


