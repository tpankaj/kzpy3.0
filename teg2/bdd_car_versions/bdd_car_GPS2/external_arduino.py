import os, serial, threading, Queue
import threading

import rospy
import std_msgs.msg
import geometry_msgs.msg
import sensor_msgs.msg
from kzpy3.utils import *

class Arduino:

    STATE_HEADING   = "hdg"
    SENSOR_STATES = (STATE_HEADING)

    def __init__(self, baudrate=115200, timeout=0.25):

        self.ser_sensors = self._setup_serial(baudrate, timeout)
        assert(self.ser_sensors is not None)

        self.state_pub = rospy.Publisher('camera_heading', std_msgs.msg.Int32, queue_size=100)

        print('Starting threads')

        threading.Thread(target=self._ros_sensors_thread).start()
    
    def _setup_serial(self, baudrate, timeout):
        sers = []
        ACM_ports = [os.path.join('/dev', p) for p in os.listdir('/dev') if 'ttyACM' in p]
        for ACM_port in ACM_ports:
            try:
                sers.append(serial.Serial(ACM_port, baudrate=baudrate, timeout=timeout))
                print('Opened {0}'.format(ACM_port))
            except:
                pass
                
        ### determine which serial port is which
        ser_sensors = None
        for ser in sers:
            for _ in xrange(100):
                try:
                    ser_str = ser.readline()
                    exec('ser_tuple = list({0})'.format(ser_str))
                    if ser_tuple[0] in Arduino.SENSOR_STATES:
                        print('Port {0} is the sensors'.format(ser.port))
                        ser_sensors = ser
                        break
                except:
                    pass
            else:
                print('Unable to identify port {0}'.format(ser.port))
        
        return ser_sensors




    def _ros_sensors_thread(self):
        """
        Receives message from sensors serial and publishes to ros
        """
        info = dict()
        
        while not rospy.is_shutdown():
            try:
            
                sensors_str = self.ser_sensors.readline()
                exec('sensors_tuple = list({0})'.format(sensors_str))

                if sensor == Arduino.STATE_HEADING:
                    assert(len(sensors_tuple) == 2)
                    gps_msg = sensor_msgs.msg.NavSatFix(longitude=data[0], latitude=data[1])
                    gps_msg.header.stamp = rospy.Time.now()
                    self.gps_pub.publish(gps_msg)

            except Exception as e:
                pass

            


