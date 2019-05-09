from __future__ import division
from webthing import (Action, Event, Property, SingleThing, Thing, Value)
import logging
import time
import uuid
import tornado.ioloop
import sensorBME680


class WeatherstationBME680(Thing):

    def __init__(self):
        Thing.__init__(self,
                       'Indoor Weatherstation',
                       ['MultiLevelSensor'],
                       'A web connected weatherstation')

        self.level = Value('Default')
        self.add_property(
            Property(
                self,
                'level',
                self.level,
                metadata={
                    '@type': 'LevelProperty',
                    'title': 'Air Quality',
                    'type': 'string',
                    'description': 'The current air quality',
                    'readOnly': True,
                }))

        logging.debug('starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update_level,
            3000
        )
        self.timer.start()

    def update_level(self):
        new_level = sensorBME680.update_air_quality()
        logging.debug('setting new air quality: %s', new_level)
        self.level.notify_of_external_update(new_level)

    def cancel_update_level_task(self):
        self.timer.stop()

