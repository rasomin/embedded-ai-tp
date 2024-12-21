import atexit
import smbus
import traitlets
from traitlets.config.configurable import Configurable
bus = smbus.SMBus(1)

Motor_ADD = 0x1B


class Motor(Configurable):

    value = traitlets.Float()
    
    # config
    alpha = traitlets.Float(default_value=1.0).tag(config=True)
    beta = traitlets.Float(default_value=0.0).tag(config=True)

    def __init__(self, driver, channel, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)  # initializes traitlets

        self._driver = driver
        self._motor = channel
        atexit.register(self._release)
        
    @traitlets.observe('value')
    def _observe_value(self, change):
        self._write_value(change['new'])

    def _write_value(self, value):
        """Sets motor value between [-1, 1]"""
        mapped_value = int(255.0 * (self.alpha * value + self.beta))
        speed = min(max(abs(mapped_value), 0), 255)
        #self._motor.setSpeed(speed)
        if mapped_value > 0:
            forward = [1,speed]
            bus.write_i2c_block_data(Motor_ADD,0x03+self._motor,forward)
            #self._motor.run(Adafruit_MotorHAT.FORWARD)
        else:
            backward = [0,speed]
            bus.write_i2c_block_data(Motor_ADD,0x03+self._motor,backward)
            #self._motor.run(Adafruit_MotorHAT.BACKWARD)

    def _release(self):
        """Stops motor by releasing control"""
        bus.write_byte_data(Motor_ADD,0x02,0x00)
