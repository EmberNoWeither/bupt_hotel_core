from ...EnviromenSim.__base__.__BaseTimer import BaseTimer as Timer
from ...EnviromenSim.__AirConditioningSim import AirConditioning
from ...utils.BaseValue import AC_Control
import copy

class BaseController(object):
    def __init__(self, Object : AirConditioning, **kwds) -> None:
        self.__total_cost = 0
        self.__power_usage = 0
        self.__status_show = {
            'total_cost' : copy.copy(self.__total_cost),
            'power_usage' : copy.copy(self.__power_usage),
        }
        self.__now_operate = AC_Control.Close
        
        for key, value in zip(list(kwds.keys()), list(kwds.values())):
            self.__status_show[key] = value
        
    
    def __call__(self):
        return self.__status_show
    
    
    def operate_control(self, control_set):
        pass