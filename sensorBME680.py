import bme680

sensor = bme680.BME680(0x77)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

def update_temperature():
    if not sensor.get_sensor_data():
        output = sensor.data.temperature
        return output
    else:
        return 999


def update_humidity():
    if sensor.get_sensor_data():
        output = sensor.data.humidity
        return output
    else:
       return -1


def update_pressure():
    if sensor.get_sensor_data():
        output = sensor.data.pressure
        return output
    else:
        return 0


def update_gas_resistance():
    if sensor.get_sensor_data():
        if sensor.data.heat_stable():
            output = sensor.data.gas_resistance
            return output
    else:
        return -1


def update_air_quality():
    hum_baseline = 40
    gas_baseline = 50000

    hum = update_humidity()
    gas = update_gas_resistance()

    if hum == -1 or gas == 0:
        return "Unknown"

    hum_offset = hum - hum_baseline
    gas_offset = gas_baseline - gas

    if hum_offset > 0:
        hum_score = (100 - hum_baseline - hum_offset)
        hum_score /= (100 - hum_baseline)
        hum_score *= (0.25 * 100)

    else:
        hum_score = (hum_baseline + hum_offset)
        hum_score /= hum_baseline
        hum_score *= (0.25 * 100)

    if gas_offset > 0:
        gas_score = (gas / gas_baseline)
        gas_score *= (100 - (0.75 * 100))

    else:
        gas_score = 100 - (0.75 * 100)

    air_quality_score = hum_score + gas_score

    if 20 > air_quality_score >= 0:
        return "Very Bad"
    else:
        if 40 > air_quality_score >= 20:
            return "Bad"
        else:
            if 60 > air_quality_score >= 40:
                return "Little Bad"
            else:
                if 80 > air_quality_score >= 60:
                    return "Average"
                else:
                    return "Good"
