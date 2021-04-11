import ure

crc16_tab = []

def crc16(data : bytearray, offset : int, length: int):
    if data is None or offset < 0 or offset > len(data)-1 and offset+length > len(data):
        return 0

    if len(crc16_tab) == 0:
        for i in range(0, 256):
            crc = i
            for j in range(0, 8):
                if (crc & 0x0001):
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
            crc16_tab.append(hex(crc))

    crcValue = 0    

    for i in range(0, length):
        tmp = crcValue ^ data[offset + i]
        rotated = crcValue >> 8
        crcValue = rotated ^ int(crc16_tab[(tmp & 0x00ff)], 0)

    return crcValue

checksum_regex = ure.compile('\r\n!(....)\r\n')
def validate_checksum(telegram_data):
    crc_result = checksum_regex.search(telegram_data.decode())

    if crc_result is None:
        raise Exception("No checksum found in telegram")

    given_crc = hex(int(crc_result.group(1), 16))

    calculated_crc = hex(crc16(telegram_data, 0, len(telegram_data) - 6))

    if given_crc != calculated_crc:
        raise Exception("Given checksum: {}, Calculated checksum: {}".format(given_crc, calculated_crc))