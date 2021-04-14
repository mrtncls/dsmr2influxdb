import time
from dsmr_reader import read as read_dsmr
from wifi import connect as connect_wifi
from influxdb import write as write_to_influx

def start_webrepl():
    # run 'import webrepl_setup' from repl and setup a password
    import webrepl
    webrepl.start()

def main():

    try:
        connect_wifi()
        start_webrepl()
    except Exception as e:
        print('Resetting... Connect error: {}'.format(e))
        machine.reset()

    while True:
        
        try:
            connect_wifi()
        except Exception as e:
            print('Resetting... Connect error: {}'.format(e))
            machine.reset()

        telegram = None
        try:
            telegram = read_dsmr()
        except Exception as e:
            print('Receive telegram error: {}'.format(e))

        if telegram:
            try:
                write_to_influx(telegram)
            except Exception as e:
                print('Write telegram error: {}'.format(e))

        time.sleep(5)

if __name__ == '__main__':
    main()
