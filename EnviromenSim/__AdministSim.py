from __PeopleSimulator import PeopleSimulator as People
from ..utils.BaseValue import PA
import copy


class AdministSimulator(People):
    def __init__(self, phone_number, id_card, sign_time) -> None:
        super().__init__(phone_number, id_card, sign_time)
        self.__property = copy.deepcopy(self.property)
        self.set_property('Authority', PA.administ)
        
        
    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)