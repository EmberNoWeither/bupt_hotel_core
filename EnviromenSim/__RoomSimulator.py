from __base__.__BaseSimulator import BaseSimulator
from __RoomerSim import RoomerSimulator as Roomer
from __AirConditioningSim import AirConditioning
from math import*
from ..utils.BaseValue import ROOM_STATUS, AC_STATUS


class RoomSimulator(BaseSimulator):
    def __init__(self, room_id:int, room_tmp, out_tmp) -> None:
        super().__init__()
        
        self.__property = {
            'room_id' : room_id,
            'status' : ROOM_STATUS.ava,
            'room_tmp' : room_tmp ,
            'out_tmp' : out_tmp,
            'roomer' : None,
        }
        
        self.__K = 0.33
        
        self.ac = AirConditioning(room_id)
        
    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)
    
    
    def check_in_room(self, people : Roomer):
        self.__property['roomer'] = people
        self.__property['status'] = ROOM_STATUS.using
        
        
    def check_out_room(self):
        self.__property['roomer'] = None
        self.__property['status'] = ROOM_STATUS.ava
        
        
    def tmp_simulating(self):
        self.__property['room_tmp'] = self.__K * self.__property['out_tmp'] + (1 - self.__K) * self.__property['room_tmp']
        
        if self.ac(attr='status') == AC_STATUS.Running:
            power, output = self.ac.condition_running(room_tmp = self.__property['room_tmp'])
            self.__property['room_tmp'] += output
            
        return power
        
        