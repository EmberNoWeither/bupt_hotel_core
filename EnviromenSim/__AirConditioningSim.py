from __base__.__BaseSimulator import BaseSimulator
from __base__.__BaseTimer import BaseTimer
from ..utils.BaseValue import AC_STATUS
from ..utils.BaseValue import AC_MODE, WIND_SPEED
from math import*


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
        self.__output_limit = 0.02
        
    def __call__(self, target, now):
        return self.PID_Calculate(target, now)
        
    def PID_Calculate(self, target, now):
        
        target = self.__filter_ratio * target + (1 - self.__filter_ratio) * now     # 对输入目标值做一阶低通滤波
        
        error = target - now
        if error <= self.__deadband:
            return 0
        
        # 前馈和比例输出
        k_out = self.__k * now * error / (fabs(error) + 1e-5)
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
            'mode' : None,
            'set_tmp' : 26,
            'wind_spd' : None,
            'wind_drc' : None,
            'sweep_mode' : None,
            'power_usage' : 0,
        }
        
        self.__power_mode = {
            AC_MODE.Cold : 100,
            AC_MODE.Hot : 200,
            AC_MODE.Wind : 0,       # 通风由风速决定功率
            AC_MODE.Dry : 60
        }
        
        self.__power_spd = {
            WIND_SPEED.slow : 5,
            WIND_SPEED.middle : 10,
            WIND_SPEED.high : 20,
            WIND_SPEED.super : 30
        }
        
        self.__pid = PID(0.5,0,0,0)
        
    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)
    
    
    def __control_tmp(self, room_tmp):
        if self.__property['mode'] != AC_MODE.Cold or self.__property['mode'] != AC_MODE.Hot:
            raise "Error Mode Set!"
        
        output = self.__pid(self.__property['set_tmp'], room_tmp)
        return output
    
        
    def condition_running(self, **kwds):
        power = 0
        output = 0
        if self.__property['mode'] == AC_MODE.Cold:
            try:
                room_tmp = kwds['room_tmp']
                set_tmp = self.__property['set_tmp']
                
                output = self.__control_tmp(room_tmp)
                
                if set_tmp >= room_tmp:
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
                
                output = self.__control_tmp(room_tmp)
                
                if set_tmp <= room_tmp:
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
            
        self.set_property('now_power', power)
        
        return power, output