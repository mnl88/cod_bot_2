import sqlalchemy as sa
from utils.db_api import TimedBaseModel


class InputDevice(TimedBaseModel):
    __tablename__ = 'test_input_devices'
    # __tablename__ = 'input_devices'
    id = sa.Column(sa.Integer, primary_key=True)  # ID
    name = sa.Column(sa.String(100), unique=True)  # mouse, Dualsense
    description = sa.Column('description', sa.String(500))  # mouse, Dualsense
    # device_type = sa.Column(sa.Integer, sa.ForeignKey('test_input_device_types.id'), nullable=True)  # mouse, gamepad
    # device_type = sa.Column(sa.Integer, sa.ForeignKey('input_device_types.id'), nullable=True)  # mouse, gamepad