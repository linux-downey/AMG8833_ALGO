'''
 * Seeed_AMG8833.py
 * Driver for DIGITAL I2C HUMIDITY AND TEMPERATURE SENSOR
 *  
 * Copyright (c) 2018 Seeed Technology Co., Ltd.
 * Website    : www.seeed.cc
 * Author     : downey
 * Create Time: June 2018
 * Change Log :
 *
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 '''

import driver
import time

PIXEL_NUM                           =64
DEFAULT_IIC_ADDR                    =0X69

POWER_CONTROL_REG_ADDR             =0X00
RESET_REG_ADDR                     =0X01
FRAME_RATE_ADDR                    =0X02
INTERRUPT_CONTROL_REG_ADDR         =0X03
STATUS_REG_ADDR                    =0X04
STATUS_CLEAR_REG_ADDR              =0X05
AVERAGE_REG_ADDR                   =0X07
INT_LEVEL_REG_ADDR_HL              =0X08
INT_LEVEL_REG_ADDR_HH              =0X09
INT_LEVEL_REG_ADDR_LL              =0X0A
INT_LEVEL_REG_ADDR_LH              =0X0B
INT_LEVEL_REG_ADDR_YSL             =0X0C
INT_LEVEL_REG_ADDR_YSH             =0X0D
THERMISTOR_REG_ADDR_L              =0X0E
THERMISTOR_REG_ADDR_H              =0X0F
INTERRUPT_TABLE_1_8_REG_ADDR       =0X10
INTERRUPT_TABLE_9_16_REG_ADDR      =0X11
INTERRUPT_TABLE_17_24_REG_ADDR     =0X12
INTERRUPT_TABLE_25_32_REG_ADDR     =0X13
INTERRUPT_TABLE_33_40_REG_ADDR     =0X14
INTERRUPT_TABLE_41_48_REG_ADDR     =0X15
INTERRUPT_TABLE_49_56_REG_ADDR     =0X16
INTERRUPT_TABLE_57_64_REG_ADDR     =0X17

TEMPERATURE_REG_ADDR_L             =0X80
TEMPERATURE_REG_ADDR_H             =0X81


INT_ACTIVE                          =0X01
INT_ABS_VALUE_INT_MODE              =0X02

NORMAL_MODE                         =0X00
SLEEP_MODE                          =0X10
STAND_BY_MODE_60S_INTERMITTENCE     =0X20
STAND_BY_MODE_10S_INTERMITTENCE     =0X21


CLEAR_ALL_STATUS                    =0X0E
CLEAR_INTERRUPT_STATUS              =0X02

INIT_RESET_VALUE                    =0X3F
FLAG_RESET_VALUE                    =0X30



class AMG8833(object):
    def __init__(self,addr=DEFAULT_IIC_ADDR):
        bus_num=driver.get_default_bus()
        self.device=driver.get_i2c_device(addr,bus_num)

        self.set_sensor_mode(NORMAL_MODE)
        self.clear_status(CLEAR_ALL_STATUS)
        self.reset_flags(INIT_RESET_VALUE)

        #upper_data=[0x80,0x00]
        #self.set_upper_limit(upper_data)

        #lower_limit=[0x01,0x00]
        #self.set_lower_limit(lower_limit)
        
        #hysteresis=[0x7f,0x00]
        #self.set_hysteresis(hysteresis)

    def set_sensor_mode(self,mode):
        self.device.write8(POWER_CONTROL_REG_ADDR,mode)
    def clear_status(self,value):
        self.device.write8(STATUS_CLEAR_REG_ADDR,value)
    def reset_flags(self,value):
        self.device.write8(RESET_REG_ADDR,value)
    def set_interrupt_mode(self,mode):
        self.device.write8(INTERRUPT_CONTROL_REG_ADDR,mode)
    def set_upper_limit(self,data):
        self.device.write8(INT_LEVEL_REG_ADDR_HL,data[0])
        self.device.write8(INT_LEVEL_REG_ADDR_HH,data[1])
    def set_lower_limit(self,data):
        self.device.write8(INT_LEVEL_REG_ADDR_LL,data[0])
        self.device.write8(INT_LEVEL_REG_ADDR_LH,data[1])
    def set_hysteresis(self,data):
        self.device.write8(INT_LEVEL_REG_ADDR_YSL,data[0])
        self.device.write8(INT_LEVEL_REG_ADDR_YSH,data[1])
    def read_temp(self):
        buf = []
        for i in range(0, PIXEL_NUM):
            raw = self.device.readU16(TEMPERATURE_REG_ADDR_L + (i << 1))
			
            converted = self.twoCompl12(raw) * 0.25
            buf.append(converted)

        return buf
    def twoCompl12(self, val):
		if  0x7FF & val == val:
			return float(val)
		else:
			return float(val-4096 )


if __name__ == '__main__':
    sensor = AMG8833()
    time.sleep(0.5)
    buf=sensor.read_temp()
    print buf