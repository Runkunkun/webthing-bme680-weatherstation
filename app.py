from __future__ import division
from webthing import (SingleThing, WebThingServer)
import logging
import weatherstationbme680


def run_server():
    weatherstation = weatherstationbme680.WeatherstationBME680()

    server = WebThingServer(SingleThing(weatherstation), port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
