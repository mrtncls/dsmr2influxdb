import ure

float_regex = ure.compile('\(0*(\d+\.\d+)\**.*\)') 
def parseFloat(value):
    match = float_regex.search(value)

    if match:
        return match.group(1)
    
    raise Exception('Failed to parse float {}'.format(value))

int_regex = ure.compile('\(0*(\d+)\**.*\)') 
def parseInt(value):
    match = int_regex.search(value)

    if match:
        return match.group(1)
    
    raise Exception('Failed to parse int {}'.format(value))

string_regex = ure.compile('\((.*)\)') 
def parseString(value):
    match = string_regex.search(value)

    if match:
        return match.group(1)
    
    raise Exception('Failed to parse string {}'.format(value))
