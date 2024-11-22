from .__base__.__BaseSimulator import BaseSimulator
from .__base__.__BaseTimer import BaseTimer
from utils.BaseValue import AC_STATUS, PA, AC_CTROL
from utils.BaseValue import AC_MODE, WIND_SPEED,WIND_DRC,base_ratio
from math import*
import copy
from InforTransfer.__ControlMsg import ControlMsg as CtrlMsg
from InforTransfer.__base__.__BaseTransfer import condition_transfer
from utils.pymysql.database_operations import *
import datetime

class PID(object):
    def __init__(self, kp, ki, kd, k) -> None:
        self.__kp = kp
        self.__ki = ki
        self.__kd = kd
        self.__k = k
        
        self.__last_error = 0
        self.__integral = 0
        self.__deadband = 1
        
        self.__integral_limit = 10
        self.__filter_ratio = 0.75
        self.__output_limit = 0.3
        
    def __call__(self, target, now):
        return self.PID_Calculate(target, now)
        
    def PID_Calculate(self, target, now):
        
        # target = self.__filter_ratio * target + (1 - self.__filter_ratio) * now     # 对输入目标值做一阶低通滤波
        
        error = target - now
        
        # if error <= self.__deadband:
        #     return 0
        # 前馈和比例输出
        k_out = self.__k * target * error / (fabs(error) + 1e-5)
        kp_out = self.__kp * error
        
        # 积分输出
        self.__integral += error
        if fabs(self.__integral) > self.__integral_limit:
            self.__integral = self.__integral_limit * self.__integral / fabs(self.__integral)
        ki_out = self.__ki * self.__integral
        
        # 微分输出
        derative = error - self.__last_error
        kd_out = self.__kd * derative
        
        output = k_out + kp_out + ki_out + kd_out
        if fabs(output) > self.__output_limit:
            output = self.__output_limit * output / fabs(output)
        
        return output
        


class AirConditioning(BaseSimulator):
    def __init__(self, room_id) -> None:
        super().__init__()
        
        self.__property = {
            'room_id' : room_id,
            'status' : AC_STATUS.Stop,
            'now_power' : 0,
            'mode' : AC_MODE.Hot,
            'set_tmp' : 22,
            'wind_spd' : WIND_SPEED.middle,
            'wind_drc' : WIND_DRC.stay,
            'power_usage' : 0,
            "error_detail" : ""
        }
        
        self.__last_property = {
            
        }
        
        self.__power_mode = {
            AC_MODE.Cold : 10,
            AC_MODE.Hot : 20,
            AC_MODE.Wind : 0,       # 通风由风速决定功率
            AC_MODE.Dry : 6
        }
        
        self.__power_spd = {
            WIND_SPEED.slow : 0.5,
            WIND_SPEED.middle : 1,
            WIND_SPEED.high : 2,
            WIND_SPEED.super : 3
        }
        
        self.__air_cost_ratio = base_ratio
        self.__change_temp_rate = 0.5
        
        self.__pid = PID(10,0.5,0,0)
        
        
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
            
    def change_status(self, status):
        self.__property['status'] = status
    
    
    def __control_tmp(self, room_tmp):
        if self.__property['mode'] != AC_MODE.Cold and self.__property['mode'] != AC_MODE.Hot:
            raise "Error Mode Set!"
        
        output = self.__pid(self.__property['set_tmp'], room_tmp)
        return output
    
    
    def _get_air_cost_ratio(self):
        return self.__air_cost_ratio
    
    
    def make_specifications(self):
        records = {
            'room_id' : self.__property['room_id'],
            'status' : self.__property['status'],
            'now_power' : self.__property['now_power'],
            'mode' : self.__property['mode'],
            'set_tmp' : self.__property['set_tmp'],
            'wind_spd' : self.__property['wind_spd'],
            'wind_drc' : self.__property['wind_drc'],
            'power_usage' : self.__property['power_usage'],
            'process_time' : datetime.datetime.now()
        }
        return records

    
    def check_status_change(self):
        is_change = False
        status_keys = ['status','mode','set_tmp','wind_spd','wind_drc']
        for key in status_keys:
            if self.__last_property[key] != self.__property[key]:
                is_change = True
                break
            
        return is_change
    
    
    def command_response(self, command:CtrlMsg, roomer):
        
        self.__last_property = copy.deepcopy(self.__property)
        
        if command._get_authority() == PA.roomer:
            if command._get_type() == AC_CTROL.Open:
                if command._get_value()['mode']:
                    self.__property['mode'] = command._get_value()['mode']
                if command._get_value()['set_tmp'] != None:
                    self.__property['set_tmp'] = command._get_value()['set_tmp'] 
                if command._get_value()['wind_spd'] != None:
                    self.__property['wind_spd'] = command._get_value()['wind_spd']
                if command._get_value()['wind_drc'] != None:
                    self.__property['wind_drc'] = command._get_value()['wind_drc']
                self.__property['status'] = AC_STATUS.Running
                
            elif command._get_type() == AC_CTROL.Close:
                self.__property['status'] = AC_STATUS.Stop

            elif command._get_type() == AC_CTROL.SetTemp:
                if command._get_value()['mode']:
                    self.__property['mode'] = command._get_value()['mode']
                self.__property['set_tmp'] = command._get_value()['set_tmp']
                if command._get_value()['wind_spd'] != None:
                    self.__property['wind_spd'] = command._get_value()['wind_spd']
                if command._get_value()['wind_drc'] != None:
                    self.__property['wind_drc'] = command._get_value()['wind_drc']
                self.__property['status'] = AC_STATUS.Running
                
            elif command._get_type() == AC_CTROL.SetWindSpd:
                if self.__property['status'] == AC_STATUS.Running:
                    if command._get_value()['mode']:
                        self.__property['mode'] = command._get_value()['mode']
                    if command._get_value()['set_tmp'] != None:
                        self.__property['set_tmp'] = command._get_value()['set_tmp'] 
                    if command._get_value()['wind_spd'] != None:
                        self.__property['wind_spd'] = command._get_value()['wind_spd']
                    if command._get_value()['wind_drc'] != None:
                        self.__property['wind_drc'] = command._get_value()['wind_drc']
                    
            elif command._get_type() == AC_CTROL.SetWindDirect:
                if self.__property['status'] == AC_STATUS.Running:
                    if command._get_value()['mode']:
                        self.__property['mode'] = command._get_value()['mode']
                    if command._get_value()['set_tmp'] != None:
                        self.__property['set_tmp'] = command._get_value()['set_tmp'] 
                    if command._get_value()['wind_spd'] != None:
                        self.__property['wind_spd'] = command._get_value()['wind_spd']
                    if command._get_value()['wind_drc'] != None:
                        self.__property['wind_drc'] = command._get_value()['wind_drc']
                    
            elif command._get_type() == AC_CTROL.ReportError:
                self.__property['status'] = AC_STATUS.Error
                
            elif command._get_type() == AC_CTROL.SetMode:
                self.__property['mode'] = command._get_value()['mode']
                self.__property['set_tmp'] = command._get_value()['set_tmp']
                self.__property['wind_spd'] = command._get_value()['wind_spd']
                self.__property['wind_drc'] = command._get_value()['wind_drc']
                self.__property['status'] = AC_STATUS.Running
                
            elif command._get_type() == AC_CTROL.ShowBill:
                pass
            elif command._get_type() == AC_CTROL.SetSweepMode:
                pass
            elif command._get_type() == AC_CTROL.ShowSpecifications:
                pass
        elif command._get_authority() == PA.administ:
            pass
        
        # 范围限制
        if self.__property['set_tmp'] > 25:
            self.__property['set_tmp'] = 25
        elif self.__property['set_tmp'] < 18:
            self.__property['set_tmp'] = 18
        
        if self.__property['wind_spd'] == WIND_SPEED.high:
            self.__change_temp_rate = 1
        elif self.__property['wind_spd'] == WIND_SPEED.middle:
            self.__change_temp_rate = 0.5
        elif self.__property['wind_spd'] == WIND_SPEED.slow:
            self.__change_temp_rate = 1 / 3.0
        # print(self.__property['room_id'])
        # 数据库更改空调状态并记录
        try:
            change_conditioner(id=self.__property['room_id'],
                            id_card=roomer(attr='id_card'),
                            status=self.__property['status'].value,
                            mode=self.__property['mode'].value,
                            tem=self.__property['set_tmp'],
                            wind_spd = self.__property['wind_spd'].value,
                            wind_drc = self.__property['wind_drc'].value,
                            error_detail = self.__property['error_detail']
                            )
        except:
            pass
        
        
        # 生成详单记录
        if self.check_status_change():
            records = self.make_specifications()
            self.__last_property = copy.deepcopy(self.__property)
            
    
    def type_erro_detect(self, attr='', value=None):
        if not isinstance(attr, str):
            raise "Key Value Should be string!"
        
        if value==None or self.change_mode!=True:
            print('Nothing Change! You may have none value or change_mode is False')
            return True
        
        if attr not in list(self.__property.keys()):
            print(self.__property.keys())
            print('Didn\'t have this type of __property!')
            return True
        
    def condition_running(self, **kwds):
        power = 0
        output = 0
        if self.__property['status'] == AC_STATUS.Running:
            if self.__property['mode'] == AC_MODE.Cold:
                try:
                    room_tmp = kwds['room_tmp']
                    set_tmp = self.__property['set_tmp']
                    # output = self.__control_tmp(room_tmp)
                    output = - self.__change_temp_rate 
                    
                    if set_tmp >= room_tmp:
                        output = 0
                        power += 0          #  温度过低不制冷
                    elif set_tmp < room_tmp:
                        power += self.__power_mode[AC_MODE.Cold]
                        
                    power += self.__power_spd[self.__property['wind_spd']]
                except:
                    raise "Lack of room_tmp!"
                
            elif self.__property['mode'] == AC_MODE.Hot:
                try:
                    room_tmp = kwds['room_tmp']
                    set_tmp = self.__property['set_tmp']
                    
                    # output = self.__control_tmp(room_tmp)
                    output = self.__change_temp_rate 
                    
                    if set_tmp <= room_tmp:
                        output = 0
                        power += 0          #  温度过热不制热
                    elif set_tmp > room_tmp:
                        power += self.__power_mode[AC_MODE.Hot]
                        
                    power += self.__power_spd[self.__property['wind_spd']]
                except:
                    raise "Lack of room_tmp!"
                
                
            elif self.__property['mode'] == AC_MODE.Wind:
                power += self.__power_spd[self.__property['wind_spd']]


            elif self.__property['mode'] == AC_MODE.Dry:
                power += self.__power_spd[self.__property['wind_spd']] + self.__power_mode[AC_MODE.Dry]
            
        # self.set_property('now_power', power)
        self.__property['now_power'] = power
        
        return power, output