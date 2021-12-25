from aiohttp import web
from requests import get

from data import db
from data.__all_models import SchemaWeather, Weather

from config import OW_URL, OW_API_KEY
import logging
import datetime

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s", )

logger = logging.getLogger(__name__)
routes = web.RouteTableDef()


weather_schema = SchemaWeather()

@routes.get('/')
async def index(request):
    return web.Response(text="It's work!")


@routes.get('/weather')
async def index(request):
    city = request.rel_url.query['city']
    logger.info(f"city is {city}")
    today = datetime.datetime.now().date()

    session = db.create_session()
    short = session.query(Weather).filter(Weather.city == city).filter(Weather.date == today).first()
    if short:
        short.jumps_count += 1
        session.commit()

        result = {'temp': Weather.temp, 'wind': Weather.wind}
        logger.info(f"old result is {result}")

        return web.json_response(result)
    else:
        response = get(f"{OW_URL}?q={city}&appid={OW_API_KEY}")
        data = response.json()
        temp = data['main']['temp']
        wind = data['wind']['speed']

        session.add(weather_schema.load({'city': city, 'date': today}))
        session.commit()

        result = {'temp': temp, 'wind': wind}
        logger.info(f"new result is {result}")

        return web.json_response(result)




if __name__ == '__main__':
    db.global_init()
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=7890, host='127.0.0.1')


