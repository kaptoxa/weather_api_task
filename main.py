from aiohttp import web
import json

import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s", )
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

@routes.get('/')
async def index(request):
    data = await request.json()

    from pprint import pprint
    pprint(data)

    logger.info("data!")

    answer = {"temp": -20}
    return web.json_response(answer)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=7890, host='127.0.0.1')


