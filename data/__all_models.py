import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from .db import SqlAlchemyBase
from marshmallow import Schema, fields, ValidationError, pre_load, post_load


### MODELS ###

class Weather(SqlAlchemyBase):
    __tablename__ = 'weather'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    city = sa.Column(sa.String(length=255))
    date = sa.Column(sa.Date)

    temp = sa.Column(sa.Float)
    wind = sa.Column(sa.Float)

    sa.UniqueConstraint('city', 'date')

    jumps_count = sa.Column(sa.Integer, default=0)

    def __repr__(self):
        return f"weather data {self.id} for {self.city} on {self.date}"


### SCHEMAS ###


class SchemaWeather(Schema):
    id = fields.Int(dump_only=True)
    city = fields.Str(data_key='city')
    date = fields.Date(date_key='date')

    temp = fields.Float(date_key='temp')
    wind = fields.Float(date_key='wind')

    jumps_count = fields.Int(data_key='count')

    @pre_load
    def create_key(self, data, **kwargs):
        city = data.get('city')
        if not city:
            data['city'] = 'Moscow'

        date = data.get('date')
        if not date:
            data['date'] = datetime.datetime.now().date()
            # raise exception...
        return data

    @post_load
    def make_date(self, data, **kwargs):
        return Weather(city=data['city'],
                       date=data['date'],
                       temp=data['temp'],
                       wind=data['wind'])
