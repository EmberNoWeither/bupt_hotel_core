from __base__ import BaseSimulator
import PeopleSimulator as People
from math import*

class AirConditioning(object):
    def __init__(self) -> None:
        pass


class RoomSimulator(BaseSimulator):
    def __init__(self, room_id:int) -> None:
        super().__init__()
        
        self.__property = {
            'room_id' : room_id,
            'status' : 'ava',
            'room_tmp' : 30 ,
            'out_tmp' : 35,
            'roomer' : None,
        }
        
    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)
    
    
    def check_in_room(self, people : People):
        self.__property['roomer'] = people
        self.__property['status'] = 'using'
        