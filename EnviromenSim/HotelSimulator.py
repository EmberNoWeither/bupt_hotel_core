from __base__ import BaseSimulator


class HotelSimulator(BaseSimulator):
    def __init__(self) -> None:
        super().__init__()
        self.__property = {
        'rooms_id' : [],
        'out_tmp' : 30,
        'rooms_tmp' : {},
        'administ_num' : 1,
        'super_administ_num' : 1,
        'roomer_num' : 0,
        'roomers' : [],
        'rooms' : []
        }
        
    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)