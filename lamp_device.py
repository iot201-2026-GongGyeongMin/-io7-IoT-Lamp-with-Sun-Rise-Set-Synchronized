======================================
lamp_device.py
thonny 램프 esp32의 소스코드입니다
==========================================
from IO7FuPython import ConfiguredDevice
from machine import Pin
import json
import time
import uComMgr32

relay = Pin(15, Pin.OUT, value=0)
led = Pin(2, Pin.OUT, value=0)

def publish_status():
    global lastPub
    state = 'on' if relay.value() else 'off'
    device.publishEvent('status', json.dumps({'d': {'lamp': state}}))
    lastPub = time.ticks_ms()
    print('lamp:', state)

def handleCommand(topic, msg):
    command = json.loads(msg)['d']['lamp']
    if command == 'toggle':
        relay.value(1 - relay.value())
    elif command == 'on':
        relay.on()
    elif command == 'off':
        relay.off()
    else:
        return
    led.value(relay.value())
    publish_status()

nic = uComMgr32.startWiFi('lamp1')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)
device.connect()
publish_status()

while True:
    if not device.loop():
        break
    if time.ticks_diff(time.ticks_ms(), lastPub) >= device.meta['pubInterval']:
        publish_status()
    time.sleep_ms(10)
