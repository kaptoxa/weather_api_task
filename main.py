from aiohttp import web
from requests import get

from data import db
from data.__all_models import SchemaWeather, Weather
from marshmallow import ValidationError

from config import OW_URL, OW_API_KEY
import logging
import datetime

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s", )

logger = logging.getLogger(__name__)
routes = web.RouteTableDef()


weather_schema = SchemaWeather(only=("city", "date", "temp", "wind"))

@routes.get('/')
async def index(request):
    return web.Response(text="It's work!")


@routes.get('/weather')
async def index(request):
    city = request.rel_url.query['city']
    country = request.rel_url.query['country_code']
    today = datetime.datetime.now().date()
    logger.info(f"city is {city}, date is {today}")

    session = db.create_session()
    weather = session.query(Weather).filter(Weather.city == city).filter(Weather.date == today).first()
    if weather:
        weather.jumps_count += 1
        session.commit()
        return web.json_response(weather_schema.dump(weather))
    else:
        response = get(f"{OW_URL}?q={city}&lang={country.lower()}&units=metric&appid={OW_API_KEY}")
        data = {'city': city}
        forecast = response.json()
        try:
            data['temperature'] = forecast['main']['temp']
            data['wind speed'] = forecast['wind']['speed']
        except KeyError:
            return web.Response(text='Sorry, something is broken...')

        try:
            new_weather = weather_schema.load(data)
        except ValidationError as error:
            return web.json_response(error.messages)

        session.add(new_weather)
        session.commit()
        return web.json_response(weather_schema.dump(new_weather))




if __name__ == '__main__':
    db.global_init()
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=7890, host='127.0.0.1')


