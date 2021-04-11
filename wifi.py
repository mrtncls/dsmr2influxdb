import network
import time

WIFI_SSID = 'ssid'
WIFI_PWD = '***'
WIFI_CONNECT_TIMEOUT_MS = 5000

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

def connect():    
      
    if not wifi.isconnected():
        wifi.connect(WIFI_SSID, WIFI_PWD)
        print('Connecting to {}...'.format(WIFI_SSID))

        start = time.ticks_ms()            
        while not wifi.isconnected():
            connect_duration = time.ticks_diff(time.ticks_ms(), start)
            if connect_duration > WIFI_CONNECT_TIMEOUT_MS:
                raise Exception('Timeout while connecting to {}'.format(WIFI_SSID))

        print('Connected')