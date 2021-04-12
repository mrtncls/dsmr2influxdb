import socket
import dsmr_parameter_names as param

INFLUXDB_HOST = 'host'
INFLUXDB_PORT = 8086
INFLUXDB_ORG = 'org'
INFLUXDB_BUCKET = 'bucket'
INFLUXDB_TOKEN = 'token'

tcp_socket = None

def _connect():

    global tcp_socket
    
    addr = socket.getaddrinfo(INFLUXDB_HOST, INFLUXDB_PORT)[0][-1]
    
    tcp_socket = socket.socket()
    tcp_socket.connect(addr)

def _create_write_request(line_data):

    path = '/api/v2/write?org={}&bucket={}'.format(INFLUXDB_ORG, INFLUXDB_BUCKET)

    headers = 'Host: {}\r\n'.format(INFLUXDB_HOST)
    headers += 'Content-Type: text/plain; charset=utf-8\r\n'
    headers += 'Content-Length: {}\r\n'.format(len(line_data))
    headers += 'Authorization: Token {}\r\n'.format(INFLUXDB_TOKEN)

    return 'POST {} HTTP/1.1\r\n{}\r\n{}\r\n\r\n'.format(path, headers, line_data)

def _write_influxdb(line_data):

    global tcp_socket

    retries_left = 1

    request = _create_write_request(line_data)

    while True:

        try:

            if tcp_socket is None:
                _connect()
                
            tcp_socket.send(bytes(request, 'utf8'))

            response = ''
            while True:
                data = tcp_socket.recv(100)

                if data:
                    response += str(data, 'utf8')
                                        
                    if response.endswith('\r\n\r\n'):
                        if (response.startswith('HTTP/1.1 204 No Content')):
                            print('Metrics written')
                            return
                        else:                    
                            raise Exception('POST request failed: {}'.format(response))
                else:
                    raise Exception('No response received for POST request')
                        
        except Exception as e:
            retries_left = retries_left - 1
            if tcp_socket:
                tcp_socket.close()
                tcp_socket = None
            if retries_left < 0:
                raise e

def _get_line_data(telegram, measurement, tags, fields):
    line_tags = ''
    for tag_name in tags:
        if tag_name in telegram:
            line_tags = '{},{}={}'.format(line_tags, tag_name, telegram[tag_name])

    line_fields = ''
    seperator = ''
    for field_name in fields:
        if field_name in telegram:
            line_fields = '{}{}{}={}'.format(line_fields, seperator, field_name, telegram[field_name])
            seperator = ','

    return '{}{} {}'.format(measurement, line_tags, line_fields)

def _get_electricity_line_data(telegram):
    tags = [
        param.EQUIPMENT_IDENTIFIER, 
        param.VERSION,
    ]

    fields = [
        param.E_TOTAL_CONSUMED_POWER_TARIFF_1,
        param.E_TOTAL_CONSUMED_POWER_TARIFF_2,
        param.E_TOTAL_INJECTED_POWER_TARIFF_1,
        param.E_TOTAL_INJECTED_POWER_TARIFF_2,
        param.E_POWER_CONSUMPTION,
        param.E_POWER_INJECTION,
        param.E_POWER_L1_CONSUMPTION,
        param.E_POWER_L1_INJECTION,
        param.E_CURRENT_L1,
        param.E_VOLTAGE_L1,
        param.E_POWER_L2_CONSUMPTION,
        param.E_POWER_L2_INJECTION,
        param.E_CURRENT_L2,
        param.E_VOLTAGE_L2,
        param.E_POWER_L3_CONSUMPTION,
        param.E_POWER_L3_INJECTION,
        param.E_CURRENT_L3,
        param.E_VOLTAGE_L3,
        param.E_ACTIVE_TARIFF,
        param.E_BREAKER_STATE,
        param.E_LIMITER_THRESHOLD,
        param.E_FUSE_SUPERVISION_THRESHOLD_L1,
        param.E_LONG_POWER_FAILURE_COUNT,
        param.E_SHORT_POWER_FAILURE_COUNT,
    ]

    return _get_line_data(telegram, 'electricity_meter', tags, fields)
    
def _get_gas_line_data(telegram):
    tags = [
        param.G_EQUIPMENT_IDENTIFIER, 
        param.G_DEVICE_TYPE,
    ]

    fields = [
        param.G_CONSUMPTION,
        param.G_BREAKER_STATE,
    ]

    return _get_line_data(telegram, 'gas_meter', tags, fields)

def write(telegram):
    line_data = '{}\n{}'.format(
        _get_electricity_line_data(telegram),
        _get_gas_line_data(telegram))        

    _write_influxdb(line_data)

