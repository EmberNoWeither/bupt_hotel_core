from __PeopleSimulator import PeopleSimulator as People
from ..utils.BaseValue import PA
import copy


class RoomerSimulator(People):
    def __init__(self, room_id, phone_number, id_card, sign_time) -> None:
        super().__init__(phone_number, id_card, sign_time)
        self.__property = copy.deepcopy(self.property)
        del self.property
        self.set_property('Authority', PA.roomer)
        self.add_property('room_id', room_id)
        self.add_property('total_cost', 0)
        
        
    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)