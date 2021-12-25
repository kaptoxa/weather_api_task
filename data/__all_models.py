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
    date = sa.Column(sa.Date, default=datetime.datetime.now().date())

    temp = sa.Column(sa.Float)
    wind = sa.Column(sa.Float)

    sa.UniqueConstraint('city', 'date')

    jumps_count = sa.Column(sa.Integer, default=0)

    def __repr__(self):
        return f"weather data {self.id} for {self.city} on {self.date}"


### SCHEMAS ###


class SchemaWeather(Schema):
    id = fields.Int(dump_only=True)
    city = fields.Str()
    date = fields.Date()

    temp = fields.Float(data_key='temperature')
    wind = fields.Float(data_key='wind speed')

    jumps_count = fields.Int(data_key='count')

    @pre_load
    def create_key(self, data, **kwargs):
        city = data.get('city')
        if not city:
            data['city'] = 'Moscow'
            # raise exception...
        return data

    @post_load
    def make_weather(self, data, **kwargs):
        return Weather(**data)

    class Meta:
        ordered = True