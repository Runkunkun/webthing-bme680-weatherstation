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
    output = sensor.data.temperature
    return output


def update_humidity():
    output = sensor.data.humidity
    return output


def update_pressure():
    output = sensor.data.pressure
    return output


def update_gas_resistance():
    output = sensor.data.gas_resistance
    print(output)
    return output


def update_air_quality():
    hum_baseline = 40
    gas_baseline = 520000

    hum = update_humidity()
    gas = update_gas_resistance()


    hum_offset = hum - hum_baseline
    gas_offset = gas_baseline - gas

    if hum_offset > 0:
        hum_score = (hum_baseline / hum)
        hum_score *= (0.25 * 100)

    else:
        if hum_offset < 0:
            hum_score = (hum / hum_baseline)
            hum_score *= (0.25 * 100)
        else:
            hum_score = 25

    if gas_offset > 0:
        gas_score = (gas / gas_baseline)
        gas_score *= (0.75 * 100)

    else:
        gas_score = 75

    air_quality_score = hum_score + gas_score
    return air_quality_score
