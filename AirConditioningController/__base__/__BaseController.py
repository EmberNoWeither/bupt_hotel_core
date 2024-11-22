from EnviromenSim.__base__.__BaseTimer import BaseTimer as Timer
from EnviromenSim.__AirConditioningSim import AirConditioning
from utils.BaseValue import AC_CTROL, PA
from InforTransfer.__ControlMsg import ControlMsg as CtrlMsg
from InforTransfer.__base__.__BaseTransfer import condition_transfer 
import copy

class BaseController(object):
    def __init__(self, room_id, roomer=None, **kwds) -> None:
        self.__air_cost = 0
        self.__power_usage = 0
        
        if roomer:
            self.__air_cost = roomer(attr='air_cost')
            self.__power_usage = roomer(attr='power_usages')
        
        self.__status_show = {
            'room_id' : room_id,
            'air_cost' : copy.copy(self.__air_cost),
            'power_usage' : copy.copy(self.__power_usage),
        }
        self.__now_operate = AC_CTROL.Close
        self.__control_timer = Timer()
        self.__timer_records = {
            'start_time' : [],
            'end_time' : [],
            'time_label' : [],
        }
        
        for key, value in zip(list(kwds.keys()), list(kwds.values())):
            self.__status_show[key] = value
        
    
    def __call__(self):
        return self.__status_show
    
    
    def update_show(self, shows:dict):
        for key, value in zip(list(shows.keys()), list(shows.values())):
            self.__status_show[key] = value
            
            
    def _get_cost(self):
        return self.__air_cost
    
    
    def checkout_costs(self):
        self.__air_cost = 0
        self.__power_usage = 0
    
    
    def calculate_costs_power(self, power, cost):
        self.__air_cost += cost
        self.__power_usage += power
        
        self.update_show(
            {
                'air_cost' : copy.copy(self.__air_cost),
                'power_usage' : copy.copy(self.__power_usage),
            }
        )
        
        return self.__air_cost, self.__power_usage
    
    
    def operate_command(self, room_id, command : dict, request_time = None):
        if request_time:
            control_msg = CtrlMsg(room_id, command, request_time)
        else:
            control_msg = CtrlMsg(room_id, command)
        return control_msg


            
        
    