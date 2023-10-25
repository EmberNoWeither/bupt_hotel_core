from __base__ import BaseSimulator

class PeopleSimulator(BaseSimulator):
    def __init__(self, phone_number, id_card, sign_time) -> None:
        super().__init__()
        
        self.__property = {
            'phone_number' : phone_number,
            'id_card' : id_card,
            'sign_time' : sign_time,
            'total_cost' : 0.0
        }
        
        
    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)