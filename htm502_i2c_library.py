# -*- coding: utf-8 -*-
"""
Read functions for measurement values of the HTM502 Sensor via I2c interface.

Copyright 2023 E+E Elektronik Ges.m.b.H.

Disclaimer:
This application example is non-binding and does not claim to be complete with
regard to configuration and equipment as well as all eventualities. The
application example is intended to provide assistance with the HTM502 sensor
module design-in and is provided "as is".You yourself are responsible for the
proper operation of the products described. This application example does not
release you from the obligation to handle the product safely during
application, installation, operation and maintenance. By using this application
example, you acknowledge that we cannot be held liable for any damage beyond
the liability regulations described.

We reserve the right to make changes to this application example at any time
without notice. In case of discrepancies between the suggestions in this
application example and other E+E publications, such as catalogues, the content
of the other documentation takes precedence. We assume no liability for
the information contained in this document.
"""


# pylint: disable=E0401
from smbus2 import SMBus, i2c_msg
# pylint: enable=E0401
CRC8_ONEWIRE_POLY = 0x31
CRC8_ONEWIRE_START = 0xFF
HTM502_COMMAND_READ_SINGLE_SHOT = 0x2C1B
HTM502_COMMAND_READ_SINGLE_SHOT_DIS = 0x241D  # DIS = clock stretching disabled
HTM502_COMMAND_READ_PERIODIC_MEASUREMENT = 0xE000
HTM502_COMMAND_CLEAR_REGISTER = 0x3041
HTM502_COMMAND_READ_REGISTER = 0xF32D
HTM502_COMMAND_START_PERIODIC_MEASUREMENT = 0x201E
HTM502_COMMAND_END_PERIODIC_MEASUREMENT = 0x3093
HTM502_COMMAND_SOFT_RESET = 0x30A2
HTM502_COMMAND_READ_IDENTIFICATION = 0x7029


def get_status_string(status_code):
    """Return string from status_code."""
    status_string = {
        0: "Success",
        1: "Not acknowledge error",
        2: "Checksum error",
        3: "Measurement error",
    }

    if status_code < len(status_string):
        return status_string[status_code]
    return "Unknown error"


def calc_crc8(buf, start, end):
    ''' calculate crc8 checksum  '''
    crc_val = CRC8_ONEWIRE_START
    for j in range(start, end):
        cur_val = buf[j]
        for _ in range(8):
            if ((crc_val ^ cur_val) & 0x80) != 0:
                crc_val = (crc_val << 1) ^ CRC8_ONEWIRE_POLY
            else:
                crc_val = crc_val << 1
            cur_val = cur_val << 1
    crc_val &= 0xFF
    return crc_val


class HTM502():
    """Implements communication with HTM502 over i2c with a specific address."""

    def __init__(self, i2c_address):
        self.i2c_address = i2c_address

    def get_single_shot_temp_hum(self):
        """Let the sensor take a measurement and return the temperature and humidity values."""
        i2c_response = self.wire_write_read(
            [(HTM502_COMMAND_READ_SINGLE_SHOT >> 8),
             (HTM502_COMMAND_READ_SINGLE_SHOT & 0xFF)], 6)
        if (i2c_response[2] == calc_crc8(i2c_response, 0, 2)) & (i2c_response[5] ==
                                                                 calc_crc8(i2c_response, 3, 5)):
            temperature = ((float)(i2c_response[0]) * 256 + i2c_response[1]) / 100
            humidity = ((float)(i2c_response[3]) * 256 + i2c_response[4]) / 100
            return temperature, humidity
        else:
            raise Warning(get_status_string(2))

    def get_single_shot_temp_hum_clock_stretching_disabled(self):
        """Let the sensor take a measurement and return the temperature and humidity values."""
        i2c_response = self.wire_write_read(
            [(HTM502_COMMAND_READ_SINGLE_SHOT_DIS >> 8),
             (HTM502_COMMAND_READ_SINGLE_SHOT_DIS & 0xFF)], 6)
        if (i2c_response[2] == calc_crc8(i2c_response, 0, 2)) & (i2c_response[5] ==
                                                                 calc_crc8(i2c_response, 3, 5)):
            temperature = ((float)(i2c_response[0]) * 256 + i2c_response[1]) / 100
            humidity = ((float)(i2c_response[3]) * 256 + i2c_response[4]) / 100
            return temperature, humidity
        else:
            raise Warning(get_status_string(2))

    def get_periodic_measurement_temp_hum(self):
        """Get the last measurement from the periodic measurement for temperature and humidity"""
        i2c_response = self.wire_write_read(
            [(HTM502_COMMAND_READ_PERIODIC_MEASUREMENT >> 8),
             (HTM502_COMMAND_READ_PERIODIC_MEASUREMENT & 0xFF)], 6)
        if (i2c_response[2] == calc_crc8(i2c_response, 0, 2)) & (i2c_response[5] ==
                                                                 calc_crc8(i2c_response, 3, 5)):
            temperature = ((float)(i2c_response[0]) * 256 + i2c_response[1]) / 100
            humidity = ((float)(i2c_response[3]) * 256 + i2c_response[4]) / 100
            return temperature, humidity
        else:
            raise Warning(get_status_string(2))


    def start_periodic_measurement(self):
        """starts the periodic measurement"""
        self.wire_write(
            [(HTM502_COMMAND_START_PERIODIC_MEASUREMENT >> 8),
             (HTM502_COMMAND_START_PERIODIC_MEASUREMENT & 0xFF)])

    def end_periodic_measurement(self):
        """ends the periodic measurement"""
        self.wire_write(
            [(HTM502_COMMAND_END_PERIODIC_MEASUREMENT >> 8),
             (HTM502_COMMAND_END_PERIODIC_MEASUREMENT & 0xFF)])

    def read_identification(self):
        """reads the identification number"""
        i2c_response = self.wire_write_read(
            [(HTM502_COMMAND_READ_IDENTIFICATION >> 8),
             (HTM502_COMMAND_READ_IDENTIFICATION & 0xFF)], 9)
        if i2c_response[8] == calc_crc8(i2c_response, 0, 8):
            return i2c_response
        else:
            raise Warning(get_status_string(2))

    def reset(self):
        """resets the sensor"""
        self.wire_write(
            [(HTM502_COMMAND_SOFT_RESET >> 8),
             (HTM502_COMMAND_SOFT_RESET & 0xFF)])

    def i2c_reset(self):
        """resets all the sensor"""
        write_command = i2c_msg.write(0x00, 0x06)
        with SMBus(1) as htm502_communication:
            htm502_communication.i2c_rdwr(write_command)

    def read_statusregister_1(self):
        """read statusregister 1"""
        i2c_response = self.wire_write_read(
            [(HTM502_COMMAND_READ_REGISTER >> 8),
             (HTM502_COMMAND_READ_REGISTER & 0xFF)], 3)
        if i2c_response[2] == calc_crc8(i2c_response, 0, 2):
            return i2c_response[0]
        else:
            raise Warning(get_status_string(2))

    def read_statusregister_2(self):
        """read statusregister 2"""
        i2c_response = self.wire_write_read(
            [(HTM502_COMMAND_READ_REGISTER >> 8),
             (HTM502_COMMAND_READ_REGISTER & 0xFF)], 3)
        if i2c_response[2] == calc_crc8(i2c_response, 0, 2):
            return i2c_response[1]
        else:
            raise Warning(get_status_string(2))

    def clear_statusregister_1(self):
        """clear the statusregister 1"""
        self.wire_write(
            [(HTM502_COMMAND_CLEAR_REGISTER >> 8),
             (HTM502_COMMAND_CLEAR_REGISTER & 0xFF)])

    def wire_write_read(self,  buf, receiving_bytes):
        """write a command to the sensor to get different answers like temperature values,..."""
        write_command = i2c_msg.write(self.i2c_address, buf)
        read_command = i2c_msg.read(self.i2c_address, receiving_bytes)
        with SMBus(1) as htm502_communication:
            htm502_communication.i2c_rdwr(write_command, read_command)
        return list(read_command)

    def wire_write(self, buf):
        """write to the sensor"""
        write_command = i2c_msg.write(self.i2c_address, buf)
        with SMBus(1) as htm502_communication:
            htm502_communication.i2c_rdwr(write_command)
