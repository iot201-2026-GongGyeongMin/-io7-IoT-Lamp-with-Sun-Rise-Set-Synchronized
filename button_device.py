======================================
button1_device.py
thonny 버튼 esp32의 소스코드입니다
===========================================
from IO7FuPython import ConfiguredDevice
from machine import Pin
import json
import time
import uComMgr32

button = Pin(1, Pin.IN)

nic = uComMgr32.startWiFi('button1')
device = ConfiguredDevice()
device.connect()

last_value = button.value()
lastPing = time.ticks_ms()

while True:
    if not device.loop():
        break

    if time.ticks_diff(time.ticks_ms(), lastPing) >= 30000:
        device.client.ping()
        lastPing = time.ticks_ms()

    value = button.value()
    if value != last_value:
        time.sleep_ms(20)
        if button.value() == value:
            last_value = value
            state = 'pushed' if value == 1 else 'released'
            device.publishEvent('status', json.dumps({'d': {'button': state}}))
            print('button:', state)

    time.sleep_ms(10)
