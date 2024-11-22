from .__PeopleSimulator import PeopleSimulator as People
from utils.BaseValue import PA
from utils.pymysql.database_operations import *
import copy


class RoomerSimulator(People):
    def __init__(self, room_id, phone_number, id_card, sign_time, total_cost=0, power_usages=0, air_cost=0) -> None:
        super().__init__(phone_number, id_card, sign_time)

        self.__property = {
            'phone_number' : phone_number,
            'id_card' : id_card,
            'sign_time' : sign_time,
            'Authority' : PA.roomer,
            'room_id' : room_id,
            'air_cost' : air_cost,
            'total_cost' : total_cost,
            'power_usages' : power_usages
        }
        
        #数据库房客数据登记
        data_check_in(id_card, room_id, phone_number)
        
        
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
    
    
    def update_usage(self, air_cost, power_usages, delta_time):
        self.__property['air_cost'] = air_cost
        self.__property['power_usages'] += power_usages
        self.__property['total_cost'] += air_cost + delta_time * 0.00001
        
        #* 数据库更新相关信息
        guest_update(self.__property['room_id'], air_cost, power_usages, self.__property['total_cost'])