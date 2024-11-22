from .__base__.__BaseMsg import BaseMsg as Msg
from utils.BaseValue import AC_CTROL, WIND_SPEED
import datetime

class ControlMsg(Msg):
    def __init__(self, room_id, msg: dict = None, request_time = datetime.datetime.now()) -> None:
        self.__msg = msg
        self.__room_id = room_id
        try:
            self.__type = msg['type']
            if not isinstance(self.__type, AC_CTROL):
                raise "Type Format Error! Should be AC_CTROL!"
            self.__value = msg['value']
            self.__auth = msg['authority']
            
            if self.__value['wind_spd'] == WIND_SPEED.high:
                self.__level = 3
            elif self.__value['wind_spd'] == WIND_SPEED.middle:
                self.__level = 2
            else:
                self.__level = 1
                
            self.__requestTime = request_time
            self.serve_time = 0
            self.serve_start = None # 服务开始时间
            self.endTime = None
            self.finish = False     # 可供外部调用修改的命令属性——是否完成标志
            self.working_period = 2 # 可执行时间片长
            self.waiting_time = 0   # 等待时长
            self.working_times = 0  # 已被执行次数
            self.is_working = False
            
            
        except:
            raise "ControlMsg's original msg format error!"
        
    def _get_authority(self):
        return self.__auth
    
    def update_msg(self, command):
        self.working_period = command.working_period
        self.working_times = command.working_times
        
    def sleep(self):
        self.is_working = False
        self.serve_time = 0
        
    def update_serve_start(self):
        if not self.is_working: # 如果之前处于休眠状态则更新服务开始时间
            self.serve_start = datetime.datetime.now()
            self.is_working = True
    
    def _get_room_id(self):
        return self.__room_id
    
    def _get_time(self):
        return self.__requestTime
    
    def _get_level(self):
        return self.__level
        
    def _get_type(self):
        return self.__type
    
    def _get_value(self):
        return self.__value