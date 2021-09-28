# DSMR2InfluxDB

Read telemetry data (DSMR format) from the Fluvius smart digital meter's P1 port and forward to InfluxDB.
This project uses an ESP32 with micropython firmware.

# Commissioning

[Install micropython](https://micropython.org/download/esp32/)

Use a tool like [EsPy](https://github.com/jungervin/EsPy/tree/master/EsPy/Release) or [Thonny IDE](https://thonny.org/) to copy the python files onto the ESP32.  

# Hardware

 - ESP32 (optional: with charger circuit like *Wemos d32 pro*)
 - RJ11 (6P) plug and wire
 - 1000 Ohm resistor
 - Compatible battery

Connect CTS (Pin 2) of the meter to 3v3 on the ESP32  
Connect signal ground (Pin 3) to ESP32 ground  
Connect RX (Pin 5) of the meter to pin13 on the ESP32 and connect the resistor between this pin and 3v3 (to pull-up the inverted data signal)  
Connect GND (Pin 6) to ground on ESP32  

> Optional:  
> Connect 5V (Pin 1) to 5V on ESP32 to charge the battery  
> The smart meter's 5V supply isn't powerfull enough to power a ESP32 without battery

# Remote access

WebREPL will be actived but needs to be [setup on the device](https://docs.micropython.org/en/latest/esp8266/tutorial/repl.html#webrepl-a-prompt-over-wifi).  
After setup, it can be accessed via [https://micropython.org/webrepl](https://micropython.org/webrepl) or via EsPy.

Sample output:

```log
Welcome to MicroPython!                                                                                                                               
Password:                                                                                                                                             
WebREPL connected                                                                                                                                     
>>> Metrics written                                                                                                                                   
Metrics written                                                                                                                                       
Metrics written                                                                                                                                       
Metrics written                                                                                                                                       
Metrics written                                                                                                                                       
```

# Resources

https://jensd.be/1205/linux/data-lezen-van-de-belgische-digitale-meter-met-de-p1-poort
https://github.com/ndokter/dsmr_parser
https://gathering.tweakers.net/forum/view_message/63412844
https://www.fluvius.be/sites/fluvius/files/2019-12/e-mucs_h_ed_1_3.pdf
