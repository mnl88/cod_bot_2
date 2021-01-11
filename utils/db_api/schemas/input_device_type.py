import sqlalchemy as sa
from utils.db_api import TimedBaseModel


class InputDeviceType(TimedBaseModel):
    __tablename__ = 'test_input_device_types'
    # __tablename__ = 'input_device_types'
    id = sa.Column(sa.Integer, primary_key=True)  # ID
    name = sa.Column(sa.String(100), unique=True)  # mouse, gamepad
    description = sa.Column('description', sa.String(500))  # mouse, gamepad
