from aiohttp import web
from requests import get

from config import OW_URL, OW_API_KEY
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s", )
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

@routes.get('/')
async def index(request):
    return web.Response(text="It's work!")


@routes.get('/weather')
async def index(request):
    country_code = request.rel_url.query['country_code']
    city = request.rel_url.query['city']

    logger.info(f"city is {city}")

    response = get(f"{OW_URL}?q={city}&appid={OW_API_KEY}")
    logger.info(response.json())
#    answer = {"country_code": country_code,
#              "city": city}
#    return web.json_response(answer)

    return web.json_response(response.json())

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)

    web.run_app(app, port=7890, host='127.0.0.1')


