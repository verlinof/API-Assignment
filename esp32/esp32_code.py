from machine import ADC, Pin
import ujson
import network
import utime as time
import urequests as requests
import machine
import utime

DEVICE_ID = "aiothinkers-sic"
WIFI_SSID = "UGM Insecure"
WIFI_PASSWORD = "123456789"
TOKEN = "BBUS-ViDTpurgLEsFIdRxHrk65eJzK8GLS6"

def did_receive_callback(topic, message):
    print('\n\nData Received! \ntopic = {0}, message = {1}'.format(topic, message))
    
def create_json_data(moisture, rpm):
    data = ujson.dumps({
        "device_id": DEVICE_ID,
        "moisture": moisture,
        "rpm": rpm,
        "type": "sensor"
    })
    return data

def send_data(moisture, rpm):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    url_flask = "http://192.168.243.150:5000/sensors"
    headers = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}
    headers_flask = {"Content-Type": "application/json"}
    data = {
        "moisture": moisture,
        "rpm": rpm,
    }
    response = requests.post(url, json=data, headers=headers)
    response_flask = requests.post(url_flask, json=data, headers=headers_flask)
    print("Done Sending Data!")
    print("Response:", response.text)
    print("Response:", response_flask.text)
    
wifi_client = network.WLAN(network.STA_IF)
wifi_client.active(True)
print("Connecting device to WiFi")
wifi_client.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi_client.isconnected():
    print("Connecting")
    time.sleep(0.1)
print("WiFi Connected!")

# Constant
PULSES_PER_REVOLUTION = 2
ZERO_TIMEOUT = 100000
NUM_READINGS = 2
WHEEL_CIRCUMFERENCE_M = 2.0

# Variabel global
last_time_measured = utime.ticks_us()
period_between_pulses = ZERO_TIMEOUT + 1000
period_average = ZERO_TIMEOUT + 1000

frequency_raw = 0
rpm = 0
pulse_counter = 1
period_sum = 0

amount_of_readings = 1
zero_debouncing_extra = 0
readings = [0] * NUM_READINGS
read_index = 0
total = 0
average = 0

# Inisialisasi pin sensor pada GPIO2
sensor_pin = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

def pulse_event(pin):
    global last_time_measured, period_between_pulses, period_sum
    global pulse_counter, period_average, amount_of_readings
    
    now = utime.ticks_us()
    period_between_pulses = utime.ticks_diff(now, last_time_measured)
    last_time_measured = now

    if pulse_counter >= amount_of_readings:
        period_average = period_sum // amount_of_readings
        pulse_counter = 1
        period_sum = period_between_pulses

        remapped_amount_of_readings = max(1, min(10, (40000 - period_between_pulses) // 5000))
        amount_of_readings = remapped_amount_of_readings
    else:
        pulse_counter += 1
        period_sum += period_between_pulses

# Menghubungkan interrupt pada sensor
sensor_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=pulse_event)

# Inisialisasi pin ADC untuk sensor kelembaban
sensor_moisture = machine.ADC(machine.Pin(32))
sensor_moisture.atten(machine.ADC.ATTN_11DB)

def read_moisture():
    raw_value = sensor_moisture.read()
    moisture_percent = (4095 - raw_value) * 100 // 4095 
    return moisture_percent

while True:
    current_micros = utime.ticks_us()
    
    if utime.ticks_diff(current_micros, last_time_measured) > ZERO_TIMEOUT - zero_debouncing_extra:
        frequency_raw = 0
        zero_debouncing_extra = 2000
    else:
        zero_debouncing_extra = 0
        if period_average > 0:  # Cegah ZeroDivisionError
            frequency_raw = 10000000000 // period_average
        else:
            frequency_raw = 0

    rpm = (frequency_raw // PULSES_PER_REVOLUTION) * 60
    speed_kmh = (rpm * WHEEL_CIRCUMFERENCE_M * 60) / 1000.0

    # Batasi kecepatan maksimum ke 100 km/h
    speed_kmh = min(speed_kmh, 100)

    # Membaca kelembaban
    moisture = read_moisture()
    
    send_data(moisture, speed_kmh)
    
    print("Speed:", speed_kmh, "km/h | Moisture:", moisture, "%")
    
    utime.sleep(1)


