from .__base__.__BaseSimulator import BaseSimulator

class PeopleSimulator(BaseSimulator):
    def __init__(self, phone_number, id_card, sign_time) -> None:
        super().__init__()
        self.property = {
            'phone_number' : phone_number,
            'id_card' : id_card,
            'sign_time' : sign_time,
            'Authority' : None
        }
        
        
    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)