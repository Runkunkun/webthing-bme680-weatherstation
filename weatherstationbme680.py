from __future__ import division
from webthing import (Property, Thing, Value)
import logging
import tornado.ioloop
import sensorBME680


class WeatherstationBME680(Thing):

    def __init__(self):
        Thing.__init__(self,
                       'Indoor Weatherstation',
                       ['MultiLevelSensor'],
                       'A web connected weatherstation')

        self.level = Value(0.0)
        self.add_property(
            Property(
                self,
                'level',
                self.level,
                metadata={
                    '@type': 'LevelProperty',
                    'title': 'Air Quality',
                    'type': 'number',
                    'description': 'The current air quality',
                    'minimum': 0,
                    'maximum': 100,
                    'unit': 'percent',
                    'readOnly': True,
                }))

        self.humidity = Value(0.0)
        self.add_property(
            Property(
                self,
                'humidity',
                self.humidity,
                metadata={
                    '@type': 'LevelProperty',
                    'title': 'Humidity',
                    'type': 'number',
                    'description': 'Humidity in %',
                    'minimum': 0,
                    'maximum': 100,
                    'unit': 'percent',
                    'readOnly': True,
                }))

        self.temperature = Value(0.0)
        self.add_property(
            Property(
                self,
                'temperature',
                self.temperature,
                metadata={
                    '@type': 'LevelProperty',
                    'title': 'Temperature',
                    'type': 'number',
                    'description': 'The current temperature',
                    'minimum': -20,
                    'maximum': 80,
                    'unit': 'degree celsius',
                    'readOnly': True,
                }))

        self.pressure = Value(0.0)
        self.add_property(
            Property(
                self,
                'pressure',
                self.pressure,
                metadata={
                    '@type': 'LevelProperty',
                    'title': 'Air Pressure',
                    'type': 'number',
                    'description': 'The current air pressure',
                    'minimum': 600,
                    'maximum': 1200,
                    'unit': 'pascal',
                    'readOnly': True,
                }))

        logging.debug('starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update_levels,
            3000
        )
        self.timer.start()

    def update_levels(self):
        if sensorBME680.sensor.get_sensor_data():
            new_level = sensorBME680.update_air_quality()
            logging.debug('setting new air quality: %s', new_level)
            self.level.notify_of_external_update(new_level)

            new_humidity = sensorBME680.update_humidity()
            logging.debug('setting new humidity: %s', new_humidity)
            self.humidity.notify_of_external_update(new_humidity)

            new_temperature = sensorBME680.update_temperature()
            logging.debug('setting new temperature: %s', new_temperature)
            self.temperature.notify_of_external_update(new_temperature)

            new_pressure = sensorBME680.update_pressure()
            logging.debug('setting new air pressure: %s', new_pressure)
            self.pressure.notify_of_external_update(new_pressure)

    def cancel_update_level_task(self):
        self.timer.stop()

