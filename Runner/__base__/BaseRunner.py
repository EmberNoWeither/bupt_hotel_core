from EnviromenSim.__HotelSimulator import HotelSimulator as Hotel
from utils.pymysql.database_operations import *
from utils.BaseValue import AC_CTROL, AC_MODE, AC_STATUS, PA, WIND_SPEED, base_ratio

class Runner(object):
    def __init__(self) -> None:
        self.hotel = Hotel()
    
    def Hotel_SimulatingCircule(self):
        self.hotel.Hotel_Simulating()
    
    def Hotel_CheckIn(self, room_id, phone_number, id_card):
        self.hotel.Check_In(room_id, phone_number, id_card)
    
    def Hotel_CheckOut(self, room_id, user_name, id_card):
        return self.hotel.Check_Out(room_id, user_name, id_card)
    
    def Hotel_RoomStatusGet(self, room_id):
        return self.hotel.Hotel_GetRoomStatus(room_id)
    
    def Hotel_SetCostRule(self, new_ratio):
        self.hotel.base_ratio = new_ratio
    
    def Air_Controll(self, room_id, is_on, mode, tar_temp, wind):
        wind_spd = None
        if is_on:
            if wind == 1:
                wind_spd = WIND_SPEED.slow
            elif wind == 2:
                wind_spd = WIND_SPEED.middle
            elif wind == 3:
                wind_spd = WIND_SPEED.high
            command = {
                        'type': AC_CTROL.Open,
                        'value': {
                            'mode' : AC_MODE.Hot if mode == 'hot' else AC_MODE.Cold,
                            'set_tmp' : tar_temp,
                            'wind_spd': wind_spd,
                            'wind_drc':None,
                        },
                        'authority' : PA.roomer
                    }
        
        else:
            command = {
                        'type': AC_CTROL.Close,
                        'value': {
                            'mode' : AC_MODE.Hot if mode == 'hot' else AC_MODE.Cold,
                            'set_tmp' : tar_temp,
                            'wind_spd': wind_spd,
                            'wind_drc':None,
                        },
                        'authority' : PA.roomer
                    }
        print(command)
        self.hotel.Hotel_ControlProcess(room_id, command)
    
    def Hotel_SpecificationMake(self, room_id, user_name, id_card):
        return self.hotel.Hotel_GetSpecifications(room_id, id_card)

    
    