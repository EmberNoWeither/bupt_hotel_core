from .__base__.__BaseSimulator import BaseSimulator
from .__RoomerSim import RoomerSimulator as Roomer
from .__AirConditioningSim import AirConditioning
from AirConditioningController.__base__.__BaseController import BaseController
from math import*
from utils.BaseValue import ROOM_STATUS, AC_STATUS, WIND_DRC
from utils.pymysql.database_operations import *


class RoomSimulator(BaseSimulator):
    def __init__(self, room_id:int, room_tmp, out_tmp) -> None:
        super().__init__()
        
        self.__initial_tmp = room_tmp
        
        self.__property = {
            'room_id' : room_id,
            'status' : ROOM_STATUS.ava,
            'room_tmp' : room_tmp ,
            'out_tmp' : out_tmp,
            'roomer' : None,
        }
        
        self.__K = 0.005
        self.ac = AirConditioning(room_id)
        self.controller = BaseController(room_id)
        
    def __call__(self, *args: any, **kwds: any) -> any:
        if 'attr' not in list(kwds.keys()):
            try:
                kwds['show'] = True
                print(self.__property)
            except:
                pass
            return self.__property
        else:
            if kwds['attr'] not in list(self.__property.keys()):
                raise 'Didn\'t have this type of __property!, Call Error!'
            else:
                K = kwds['attr']
                return self.__property[K]
    
    
    def check_in_room(self, people : Roomer):
        self.__property['roomer'] = people
        self.__property['status'] = ROOM_STATUS.using
        self.controller = BaseController(self.__property['room_id'], self.__property['roomer'])
        
        
    def check_out_room(self):
        self.__property['roomer'] = None
        self.__property['status'] = ROOM_STATUS.ava
        
        
        #生成服务详单记录——与数据库联动
    def specifications_save(self, spe:dict):
        try:
            spe.update(id_card=self.__property['roomer'](attr='id_card'))   # 添加身份信息
            save_specifications(spe)
        except:
            pass
        
        
    def roomer_control(self, command, request_time = None):
        if request_time:
            control_msg = self.controller.operate_command(self.__property['room_id'], command, request_time)
        else:
            control_msg = self.controller.operate_command(self.__property['room_id'], command)
        self.ac.command_response(control_msg, self.__property['roomer'])
        
        return control_msg
        
        # * 此函数应在后端循环运行进行连续性环境模拟与计费
    def tmp_simulating(self, base_ratio = 1.0):
        # self.__property['room_tmp'] = self.__K * self.__property['out_tmp'] + (1 - self.__K) * self.__property['room_tmp']
        if fabs(self.__property['room_tmp'] - self.ac(attr='set_tmp')) < 1e-3 or \
            self.ac(attr='status') != AC_STATUS.Running:  #* 当温度等同于设定温度或空调未打开(或在等待调度)进行回温
                
            if fabs(self.__initial_tmp - self.__property['room_tmp']) >= 1e-3:
                self.__property['room_tmp'] += (self.__initial_tmp - self.__property['room_tmp']) / fabs(self.__initial_tmp - self.__property['room_tmp']) * 0.5

        power, output = self.ac.condition_running(room_tmp = self.__property['room_tmp'])
        
        air_cost_ratio = base_ratio

        if fabs(self.__property['room_tmp'] - self.ac(attr='set_tmp')) >= fabs(output):
            self.__property['room_tmp'] += output
            cost = output * air_cost_ratio
        else:
            cost = fabs(self.__property['room_tmp'] - self.ac(attr='set_tmp')) * air_cost_ratio
            self.__property['room_tmp'] = self.ac(attr='set_tmp')
        
        air_cost, power_usages = self.controller.calculate_costs_power(power, cost)
        
        if self.__property['roomer']:
            self.__property['roomer'].update_usage(air_cost, power_usages, 1)
            # print("room_id:%d"%self.__property['room_id'] + " air_cost:%f"%air_cost+" power_usages:%f"%power_usages+" room_tmp:%f"%self.__property['room_tmp'])

        return air_cost, power_usages, self.__property['room_id'], self.__property['room_tmp']
        
        