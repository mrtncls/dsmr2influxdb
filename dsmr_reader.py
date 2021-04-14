import ure
import time
from machine import UART, Pin
from dsmr_parameter_regex import DSMR_CONFIG
from dsmr_checksum import validate_checksum

RX = 15
RTS = 13
TX = 12 # not used
DEBUG = False
TEST = False

rts_pin = Pin(RTS, Pin.OUT)
rts_pin.value(0)

def parse(raw_data):
    telegram = {}

    for name, regex_parser in DSMR_CONFIG.items():
        regex = regex_parser[0]
        parser = regex_parser[1]
        match = ure.search(regex, raw_data.decode())

        if match:
            try:
                telegram[name] = parser(match.group(1))
            except Exception as e:
                raise Exception("Parsing failed for {}: {}".format(name, e))

    if DEBUG:
        print("Parsed:")
        print(telegram)

    return telegram    

def read():
    if TEST:
        print("*** TEST - Turn off test flag to read real data ***")
        example_telegram = bytearray(b'/FLU5\\253769484_A\r\n\r\n0-0:96.1.4(50215)\r\n0-0:96.1.1(3153414733313030323135323634)\r\n0-0:1.0.0(210408202443S)\r\n1-0:1.8.1(000360.515*kWh)\r\n1-0:1.8.2(000353.659*kWh)\r\n1-0:2.8.1(000141.617*kWh)\r\n1-0:2.8.2(000046.186*kWh)\r\n0-0:96.14.0(0001)\r\n1-0:1.7.0(00.000*kW)\r\n1-0:2.7.0(00.023*kW)\r\n1-0:21.7.0(00.319*kW)\r\n1-0:41.7.0(00.237*kW)\r\n1-0:61.7.0(00.000*kW)\r\n1-0:22.7.0(00.000*kW)\r\n1-0:42.7.0(00.000*kW)\r\n1-0:62.7.0(00.581*kW)\r\n1-0:32.7.0(236.7*V)\r\n1-0:52.7.0(236.4*V)\r\n1-0:72.7.0(238.1*V)\r\n1-0:31.7.0(001.66*A)\r\n1-0:51.7.0(001.38*A)\r\n1-0:71.7.0(002.69*A)\r\n0-0:96.3.10(1)\r\n0-0:17.0.0(999.9*kW)\r\n1-0:31.4.0(999*A)\r\n0-0:96.13.0()\r\n0-1:24.1.0(003)\r\n0-1:96.1.1(37464C4F32313230323038343530)\r\n0-1:24.4.0(1)\r\n0-1:24.2.3(210408202002S)(00371.471*m3)\r\n!DF1D\r\n')
        validate_checksum(example_telegram)
        return parse(example_telegram)

    uart = UART(1, baudrate=115200, bits=8, parity=None, stop=1, rx=RX, rxbuf=2048, tx=TX, invert=UART.INV_RX)
    raw_data = bytearray()
    found_header = False

    while True:

        if not uart.any():

            rts_pin.value(1)            
            time.sleep_ms(100)            
            rts_pin.value(0)
            
            if DEBUG:
                print('Sent RTS')

        else:

            data_line = uart.readline()
          
            if "/" in data_line:
                if DEBUG:
                    print ("Found beginning of P1 telegram")
                    print('*' * 60 + "\n")
                raw_data = bytearray()
                found_header = True

            if DEBUG:
               print ("Reading: ", data_line)

            raw_data.extend(data_line)

            if "!" in data_line:
                if DEBUG:
                    print('*' * 60 + "\n")
                    print("Found end, printing full telegram")
                    print('*' * 40)
                    print(raw_data)
                    print('*' * 40)

                if not found_header:
                    raise Exception('Header not found in telegram')
                    
                validate_checksum(raw_data)
                return parse(raw_data)