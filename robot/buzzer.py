import smbus
import time
    
def buzzer_on(count):
    bus = smbus.SMBus(1)
    Buzzer_ADD = 0x1B
    
    for _ in range(count):
        bus.write_byte_data(Buzzer_ADD, 0x06, 1)
        time.sleep(1)
        bus.write_byte_data(Buzzer_ADD, 0x06, 0)
        time.sleep(1)
        
    return

def buzzer_off():
    bus = smbus.SMBus(1)
    Buzzer_ADD = 0x1B
    
    bus.write_byte_data(Buzzer_ADD, 0x06, 0)
    return

