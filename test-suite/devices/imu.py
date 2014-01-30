import struct
from models import adis
from models import mpl

SENSORS = {
    'ADIS': {
        'rawacc': adis.acc,
        'data': {
            'endianness': '!',
            'members': [
                {'key': "VCC",     'type': "h", 'default': 0},
                {'key': "Gyro_X",  'type': "h", 'default': 0},
                {'key': "Gyro_Y",  'type': "h", 'default': 0},
                {'key': "Gyro_Z",  'type': "h", 'default': 0},
                {'key': "Acc_X",   'type': "h", 'default': 0},
                {'key': "Acc_Y",   'type': "h", 'default': 0},
                {'key': "Acc_Z",   'type': "h", 'default': 0},
                {'key': "Magn_X",  'type': "h", 'default': 0},
                {'key': "Magn_Y",  'type': "h", 'default': 0},
                {'key': "Magn_Z",  'type': "h", 'default': 0},
                {'key': "Temp",    'type': "h", 'default': 0},
                {'key': "Aux_ADC", 'type': "h", 'default': 0},
            ],
        },
    },
    'MPL': {
        'rawpressure': mpl.pressure,
        'data': {
            'endianness': '!',
            'members': [
                {'key': "?",        'type': "L", 'default': 0},
                {'key': "?",        'type': "L", 'default': 0},
            ],
        },
    },
}

class IMU(object):
    """Provides IMU data"""

    def __init__(self, source):
        self.source = source
        for fourcc, s in SENSORS.iteritems():
            struct_def = s['data']['endianness']
            s['values'] = []
            for member in s['data']['members']:
                struct_def += member['type']
                s['values'].append(member['default'])

            s['struct'] = struct.Struct(struct_def)

    def send(self, sensor, data):
        print data

    def read_sensor(self, sensor):
        s = SENSORS[sensor]
        rawdata = self.source.data()

        data = {}
        for key, value in rawdata.iteritems():
            if key in s:
                data.update(s[key](value))

        self.send(s, data)
