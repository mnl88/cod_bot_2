from sqlalchemy.orm import relationship
import sqlalchemy as sa
from utils.db_api import TimedBaseModel


class Person(TimedBaseModel):
    __tablename__ = 'test_persons'
    # __tablename__ = 'persons'

    id = sa.Column(sa.Integer, primary_key=True)  # ID
    name_or_nickname = sa.Column(sa.String(100))  # имя
    tg_account = relationship("TG_Account", backref='person', uselist=False)  # аккаунт Telegram
    activision_account = sa.Column('activision_account', sa.String(100))  # аккаунт ACTIVISION
    psn_account = sa.Column('psn_account', sa.String(100))  # аккаунт PSN
    blizzard_account = sa.Column('blizzard_account', sa.String(100))  # аккаунт Blizzard
    xbox_account = sa.Column('xbox_account', sa.String(100))  # аккаунт X-Box
    # platform = sa.Column(sa.Integer, sa.ForeignKey('test_platforms.id'), nullable=True)  # (PC, PS4, Xbox Series X)
    # platform = sa.Column(sa.Integer, sa.ForeignKey('platforms.id'), nullable=True)  # (PC, PS4, Xbox Series X)
    # input_device = sa.Column(sa.Integer, sa.ForeignKey('test_input_devices.id'), nullable=True)  # клавамышь или геймпад?
    # input_device = sa.Column(sa.Integer, sa.ForeignKey('input_devices.id'), nullable=True)  # клавамышь или геймпад?
    about_yourself = sa.Column('about_yourself', sa.String(500))  # о себе
    kd_warzone = sa.Column('kd_warzone', sa.Float(2, 2))  # КД Варзон
    kd_multiplayer = sa.Column('kd_multiplayer', sa.Float(2, 2))  # КД мультиплеер
    kd_cold_war_multiplayer = sa.Column('kd_cold_war_multiplayer', sa.Float(2, 2))  # КД Колдвар
    modified_kd_at = sa.Column('modified_kd_at', sa.TIMESTAMP)  # дата обновления статистики

    def __repr__(self):
        return "<Person: (id: '%s', nickname: '%s', tg_acc: '%s')>" % (self.id, self.name_or_nickname, self.tg_account)

    def full_print(self):
        return "<Person: (id: '%s', nickname: '%s', tg_acc: '%s')>" % (self.id, self.name_or_nickname, self.tg_account)


