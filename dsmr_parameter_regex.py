import ure
from dsmr_valueparser import parseFloat, parseInt, parseString
import dsmr_parameter_names as names

# Belgian Fluvius parameters: https://www.fluvius.be/sites/fluvius/files/2019-12/e-mucs_h_ed_1_3.pdf

# Example raw telegram:
#
# '/FLU5\\253769484_A\r\n'
# '\r\n'
# '0-0:96.1.4(50215)\r\n'
# '0-0:96.1.1(3153414733313030323135323634)\r\n'
# '0-0:1.0.0(210408202443S)\r\n'
# '1-0:1.8.1(000360.515*kWh)\r\n'
# '1-0:1.8.2(000353.659*kWh)\r\n'
# '1-0:2.8.1(000141.617*kWh)\r\n'
# '1-0:2.8.2(000046.186*kWh)\r\n'
# '0-0:96.14.0(0001)\r\n'
# '1-0:1.7.0(00.000*kW)\r\n'
# '1-0:2.7.0(00.023*kW)\r\n'
# '1-0:21.7.0(00.319*kW)\r\n'
# '1-0:41.7.0(00.237*kW)\r\n'
# '1-0:61.7.0(00.000*kW)\r\n'
# '1-0:22.7.0(00.000*kW)\r\n'
# '1-0:62.7.0(00.581*kW)\r\n'
# '1-0:32.7.0(236.7*V)\r\n'
# '1-0:52.7.0(236.4*V)\r\n'
# '1-0:72.7.0(238.1*V)\r\n'
# '1-0:31.7.0(001.66*A)\r\n'
# '1-0:51.7.0(001.38*A)\r\n'
# '1-0:71.7.0(002.69*A)\r\n'
# '0-0:96.3.10(1)\r\n'
# '0-0:17.0.0(999.9*kW)\r\n'
# '1-0:31.4.0(999*A)\r\n'
# '0-0:96.13.0()\r\n'
# '0-1:24.1.0(003)\r\n'
# '0-1:96.1.1(37464C4F32313230323038343530)\r\n'
# '0-1:24.4.0(1)\r\n'
# '0-1:24.2.3(210408202002S)(00371.471*m3)\r\n'
# '!DF1D\r\n'

EQUIPMENT_IDENTIFIER_REGEX = ure.compile('0-0:96\.1\.1(.+?)\r\n')
VERSION_REGEX = ure.compile('0-0:96\.1\.4(.+?)\r\n') # E.g. DSMR P1 v5.0.2 and e-MUCS H v1.0 gives the value ‘50210’ as version information)
TIMESTAMP_REGEX = ure.compile('0-0:1\.0\.0(.+?)\r\n')
MESSAGE_REGEX = ure.compile('0-0:96\.13\.0(.+?)\r\n')
E_TOTAL_CONSUMED_POWER_TARIFF_1_REGEX = ure.compile('1-0:1\.8\.1(.+?)\r\n')
E_TOTAL_CONSUMED_POWER_TARIFF_2_REGEX = ure.compile('1-0:1\.8\.2(.+?)\r\n')
E_TOTAL_INJECTED_POWER_TARIFF_1_REGEX = ure.compile('1-0:2\.8\.1(.+?)\r\n')
E_TOTAL_INJECTED_POWER_TARIFF_2_REGEX = ure.compile('1-0:2\.8\.2(.+?)\r\n')
E_POWER_CONSUMPTION_REGEX = ure.compile('1-0:1\.7\.0(.+?)\r\n')
E_POWER_INJECTION_REGEX = ure.compile('1-0:2\.7\.0(.+?)\r\n')
E_POWER_L1_CONSUMPTION_REGEX = ure.compile('1-0:21\.7\.0(.+?)\r\n')
E_POWER_L1_INJECTION_REGEX = ure.compile('1-0:22\.7\.0(.+?)\r\n')
E_CURRENT_L1_REGEX = ure.compile('1-0:31\.7\.0(.+?)\r\n')
E_VOLTAGE_L1_REGEX = ure.compile('1-0:32\.7\.0(.+?)\r\n')
E_POWER_L2_CONSUMPTION_REGEX = ure.compile('1-0:41\.7\.0(.+?)\r\n')
E_POWER_L2_INJECTION_REGEX = ure.compile('1-0:42\.7\.0(.+?)\r\n')
E_CURRENT_L2_REGEX = ure.compile('1-0:51\.7\.0(.+?)\r\n')
E_VOLTAGE_L2_REGEX = ure.compile('1-0:52\.7\.0(.+?)\r\n')
E_POWER_L3_CONSUMPTION_REGEX = ure.compile('1-0:61\.7\.0(.+?)\r\n')
E_POWER_L3_INJECTION_REGEX = ure.compile('1-0:62\.7\.0(.+?)\r\n')
E_CURRENT_L3_REGEX = ure.compile('1-0:71\.7\.0(.+?)\r\n')
E_VOLTAGE_L3_REGEX = ure.compile('1-0:72\.7\.0(.+?)\r\n')
E_ACTIVE_TARIFF_REGEX = ure.compile('0-0:96\.14\.0(.+?)\r\n')
E_BREAKER_STATE_REGEX = ure.compile('0-0:96\.3\.10(.+?)\r\n')
E_LIMITER_THRESHOLD_REGEX = ure.compile('0-0:17\.0\.0(.+?)\r\n')
E_FUSE_SUPERVISION_THRESHOLD_L1_REGEX = ure.compile('1-0:31\.4\.0(.+?)\r\n')
E_LONG_POWER_FAILURE_COUNT_REGEX = ure.compile('96\.7\.9(.+?)\r\n')
E_SHORT_POWER_FAILURE_COUNT_REGEX = ure.compile('96\.7\.21(.+?)\r\n')
G_DEVICE_TYPE_REGEX = ure.compile('0-1:24\.1\.0(.+?)\r\n')
G_EQUIPMENT_IDENTIFIER_REGEX = ure.compile('0-1:96\.1\.1(.+?)\r\n')
G_CONSUMPTION_REGEX = ure.compile('0-1:24\.2\.3(.+?)\r\n')
G_BREAKER_STATE_REGEX = ure.compile('0-1:24\.4\.0(.+?)\r\n')

DSMR_CONFIG = {
    names.EQUIPMENT_IDENTIFIER: [EQUIPMENT_IDENTIFIER_REGEX, parseString],
    names.VERSION: [VERSION_REGEX, parseString],
    # names.TIMESTAMP: [TIMESTAMP_REGEX, parseFloat],
    names.MESSAGE: [MESSAGE_REGEX, parseString],
    names.E_TOTAL_CONSUMED_POWER_TARIFF_1: [E_TOTAL_CONSUMED_POWER_TARIFF_1_REGEX, parseFloat],
    names.E_TOTAL_CONSUMED_POWER_TARIFF_2: [E_TOTAL_CONSUMED_POWER_TARIFF_2_REGEX, parseFloat],
    names.E_TOTAL_INJECTED_POWER_TARIFF_1: [E_TOTAL_INJECTED_POWER_TARIFF_1_REGEX, parseFloat],
    names.E_TOTAL_INJECTED_POWER_TARIFF_2: [E_TOTAL_INJECTED_POWER_TARIFF_2_REGEX, parseFloat],
    names.E_POWER_CONSUMPTION: [E_POWER_CONSUMPTION_REGEX, parseFloat],
    names.E_POWER_INJECTION: [E_POWER_INJECTION_REGEX, parseFloat],
    names.E_POWER_L1_CONSUMPTION: [E_POWER_L1_CONSUMPTION_REGEX, parseFloat],
    names.E_POWER_L1_INJECTION: [E_POWER_L1_INJECTION_REGEX, parseFloat],
    names.E_CURRENT_L1: [E_CURRENT_L1_REGEX, parseFloat],
    names.E_VOLTAGE_L1: [E_VOLTAGE_L1_REGEX, parseFloat],
    names.E_POWER_L2_CONSUMPTION: [E_POWER_L2_CONSUMPTION_REGEX, parseFloat],
    names.E_POWER_L2_INJECTION: [E_POWER_L2_INJECTION_REGEX, parseFloat],
    names.E_CURRENT_L2: [E_CURRENT_L2_REGEX, parseFloat],
    names.E_VOLTAGE_L2: [E_VOLTAGE_L2_REGEX, parseFloat],
    names.E_POWER_L3_CONSUMPTION: [E_POWER_L3_CONSUMPTION_REGEX, parseFloat],
    names.E_POWER_L3_INJECTION: [E_POWER_L3_INJECTION_REGEX, parseFloat],
    names.E_CURRENT_L3: [E_CURRENT_L3_REGEX, parseFloat],
    names.E_VOLTAGE_L3: [E_VOLTAGE_L3_REGEX, parseFloat],
    names.E_ACTIVE_TARIFF: [E_ACTIVE_TARIFF_REGEX, parseInt],
    names.E_BREAKER_STATE: [E_BREAKER_STATE_REGEX, parseInt],
    names.E_LIMITER_THRESHOLD: [E_LIMITER_THRESHOLD_REGEX, parseFloat],
    names.E_FUSE_SUPERVISION_THRESHOLD_L1: [E_FUSE_SUPERVISION_THRESHOLD_L1_REGEX, parseInt],
    names.E_LONG_POWER_FAILURE_COUNT: [E_LONG_POWER_FAILURE_COUNT_REGEX, parseInt],
    names.E_SHORT_POWER_FAILURE_COUNT: [E_SHORT_POWER_FAILURE_COUNT_REGEX, parseInt],
    names.G_DEVICE_TYPE: [G_DEVICE_TYPE_REGEX, parseInt],
    names.G_EQUIPMENT_IDENTIFIER: [G_EQUIPMENT_IDENTIFIER_REGEX, parseString],
    names.G_CONSUMPTION: [G_CONSUMPTION_REGEX, parseFloat],
    names.G_BREAKER_STATE: [G_BREAKER_STATE_REGEX, parseInt],
}