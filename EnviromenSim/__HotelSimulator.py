from __base__.__BaseSimulator import BaseSimulator
from __RoomSimulator import RoomSimulator as Room
from __RoomerSim import RoomerSimulator as Roomer
from ..utils.BaseOperators import list_attr_Add
from ..utils.BaseValue import ROOM_STATUS
import datetime


class HotelSimulator(BaseSimulator):
    def __init__(self, init_rooms_num = 6) -> None:
        super().__init__()
        self.__property = {
        'rooms_id' : [i for i in range(init_rooms_num)],
        'out_tmp' : 35,
        'rooms_tmp' : {},
        'administ_num' : 1,
        'super_administ_num' : 1,
        'roomer_num' : 0,
        'roomers' : [],
        'rooms' : []
        }
        
        for i in range(init_rooms_num):
            self.__property['rooms_tmp'][i] = 30
            self.__property['rooms'].append(Room(i, 30, self.__property['out_tmp']))
            
        
    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)
    
    
    def Check_In(self, rooms_id, phone_number, id_card):
        if self.__property['roomer_num'] == len(self.__property['rooms']):
            v = "很抱歉，酒店已住满，暂无房间可用！"
            print(v)
            return v
        
        roomer = Roomer(rooms_id, phone_number, id_card, datetime.datetime.now())
        self.__property['roomer_num'] += 1
        self.set_property('roomers', roomer, list_attr_Add)
        
        for room in self.__property['rooms']:
            if roomer(attr='room_id') == room(attr='room_id'):
                room.check_in_room(roomer)
                break
        
        return 1
    
    
    def Check_Out(self, rooms_id, phone_number, id_card):
        if self.__property['roomer_num'] == 0:
            print('未有房客登记！')
            return 0
        
        is_exist = False
        for roomer in self.__property['roomers']:
            if rooms_id == roomer(attr='room_id') and phone_number == roomer(attr='phone_number') \
                and id_card == roomer(attr='id_card'):
                    is_exist = True
        
                    for room in self.__property['rooms']:
                        if roomer(attr='room_id') == room(attr='room_id'):
                            room.check_out_room()
                            break
                        
                    self.__property['roomers'].remove(roomer)
                    self.__property['roomer_num'] -= 1
                    
        if is_exist:
            return 1
        else:
            print("所要退房的房客不存在！")
            return 0
                    