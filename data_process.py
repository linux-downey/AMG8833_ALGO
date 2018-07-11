import Seeed_AMG8833 
import time
import threading

import Queue
#import numpy

PIXELS_NUM            =64
FILTER_BUF_SIZE        =5
SLIDING_WINDOW_SIZE    =20

#low range of the sensor (this will be blue on the screen)
MINTEMP = 26

#high range of the sensor (this will be red on the screen)
MAXTEMP = 31


class Data_proc(object):
    def __init__(self):
        self.sensor=Seeed_AMG8833.AMG8833()
        self.filter_list=[]
        self.window_list = []
        self.filt_data = []
        self.counts = 0
        #self.timer=threading.Timer(5,self.func_timer)
        #self.timer.start()

    def get_raw_sens_data(self):
        buf=[]
        buf=self.sensor.read_temp()
        return buf
         
    def __calc_filt_data(self,list):
        aver_before = []
        aver_behind = []
        for i in range(PIXELS_NUM):
            #calculate the average of twice before
            aver_before.append(self.__calc_aver(list[0][i],list[1][i]))
            #calculate the average of twice later
            aver_behind.append(self.__calc_aver(list[3][i],list[4][i]))

            differ_before=abs(aver_before[i]-list[2][i])
            differ_behind=abs(aver_behind[i]-list[2][i])
            #if the data is deferent from the data before and after,this judges that it's a invalid data
            if((differ_before>0.75) and (differ_behind>0.75)):
                list[2][i]=aver_behind[i]
    
    def __calc_aver(self,val1,val2):
        return (val1+val2+0.25)/2

    def get_filtered_data(self,data):
        if(len(self.filter_list) != FILTER_BUF_SIZE):
            self.filter_list.append(data)
            return None
        else:
            self.filter_list.pop(0)
            self.filter_list.append(data)
            self.__calc_filt_data(self.filter_list)
            return self.filter_list[(FILTER_BUF_SIZE+1)/2]
    
    def window_aver(self):
        if(len(self.window_list) != SLIDING_WINDOW_SIZE):
            return None
        
        win_aver = []
        for i in range(PIXELS_NUM):
            sum = 0
            for j in range(SLIDING_WINDOW_SIZE):
                sum +=self.window_list[j][i]
            win_aver.append(sum/SLIDING_WINDOW_SIZE)
        return win_aver

    #A queue struct,remove the head,add to the tail.
    def put_data_to_window(self,data):
        if(len(self.window_list) != SLIDING_WINDOW_SIZE):
            self.window_list.append(data)
        else:
            self.window_list.pop(0)
            self.window_list.append(data)

    def get_final_sensor_data(self,data_win,data_filt):
        fin_data = []
        for i in range(PIXELS_NUM):
            if(data_filt[i]-data_win[i] >= 2.5):
                fin_data.append(data_filt[i])
            else:
                fin_data.append(MINTEMP)
            
        return fin_data
    
    def get_sensor_data(self):
        raw_data = []
        window_aver = []
        dest_data = [MINTEMP] * PIXELS_NUM
        #raw sensor data
        raw_data=self.get_raw_sens_data()
        '''
        self.counts += 1
        if(self.counts>=10):
            self.counts=0
            self.put_data_to_window(self.filt_data)
        '''
        #get data after filte.
        self.filt_data=self.get_filtered_data(raw_data)
                
        if self.filt_data is not None:
            #sliding window.
            window_aver=self.window_aver()
            if window_aver is not None:
                #dest data is the data to display on screen.
                dest_data = self.get_final_sensor_data(window_aver,self.filt_data)
                return dest_data
            else:
                self.put_data_to_window(self.filt_data)
                return dest_data
        else:
            return dest_data
                    
            

        





if __name__ == '__main__':
    sensor_data = []
    AMG_sensor = Data_proc()
    while 1:
        time.sleep(.1)
        sensor_data = AMG_sensor.get_sensor_data()
        print sensor_data
        '''
        data=outpt_dat.get_sens_data()
        #The data after filter.
        data=outpt_dat.get_filtered_data(data)
        if data is not None:
            window_aver= outpt_dat.window_aver()  
            if window_aver is not None:
                #print window_aver
                #print data
                #raw_data = outpt_dat.get_sens_data()
                #print max(raw_data),max(outpt_dat.get_final_sensor_data(window_aver,data))
                print max(outpt_dat.get_final_sensor_data(window_aver,data))
                #print  outpt_dat.get_final_sensor_data(window_aver,data)
            outpt_dat.put_data_to_window(data)
        '''

