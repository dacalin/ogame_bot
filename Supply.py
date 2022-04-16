import random
import numpy as np
from ogame.constants import buildings
from Config import Config

class Supply:
    def __init__(self, config: Config):
        self.config = config
        self.resources_action_map = {
                  0: buildings.metal_mine,
                  1: buildings.crystal_mine,
                  2: buildings.deuterium_mine,
                  3: buildings.solar_plant,
                  4: buildings.fusion_plant,
                  5: buildings.metal_storage,
                  6: buildings.crystal_storage,
                  7: buildings.deuterium_storage}

        self.operate = False
        self.programmed_action_code = {}

    def _maximun_reach(self, actual_resources, planet_id) -> bool:
        result = False

        max = self.config.max_supplies_resources(planet_id)

        if actual_resources.metal > max['metal'] or actual_resources.crystal > max['crystal'] or actual_resources.deuterium > max['deuterium']:
            result = True

        return result

    def _minimum_reach(self, actual_resources, planet_id) -> bool:
        result = False

        min = self.config.min_supplies_resources(planet_id)

        if actual_resources.metal > min['metal'] and actual_resources.crystal > min['crystal'] and actual_resources.deuterium > min['deuterium']:
            result = True

        return result

    def _is_posible(self, empire, planet_id, action_code) -> bool:

        sup = empire.supply(planet_id)
        ret = False

        if action_code == 0:
            ret = sup.metal_mine.is_possible
        elif action_code == 1:
            ret = sup.crystal_mine.is_possible
        elif action_code == 2:
            ret = sup.deuterium_mine.is_possible
        elif action_code == 3:
            ret = sup.solar_plant.is_possible
        elif action_code == 4:
            ret = sup.fusion_plant.is_possible
        elif action_code == 5:
            ret = sup.metal_storage.is_possible
        elif action_code == 6:
            ret = sup.crystal_storage.is_possible
        elif action_code == 7:
            ret = sup.deuterium_storage.is_possible

        return ret

    def _ensure_planet_key_exists(self, planet_id):
        if planet_id not in self.programmed_action_code:
            self.programmed_action_code[planet_id] = None


    def next(self, empire, planet_id: int):
        """
        Calculate next action

        :param empire: pyogame empire class
        :param planet_id: pyogame planet id
        :return: pyogame action
        """
        action = None

        self._ensure_planet_key_exists(planet_id)

        actual_resources = empire.resources(planet_id)

        max = self._maximun_reach(actual_resources, planet_id)
        min = self._minimum_reach(actual_resources, planet_id)

        if max and not self.operate:
            self.operate = True

        if self.operate and not min:
            self.operate = False

        if self.operate:

            if self.programmed_action_code[planet_id] is not None:
                action_code = self.programmed_action_code[planet_id]
                self.programmed_action_code[planet_id] = None

            else:
                number = random.random()*100

                resources_probability = self.config.supplies_probabilities(planet_id)

                # metal_prob, crystal_prob, deuterium_prob, solar_prob, fusion_prob, metal_st_prob,crystal_st_prob, deuterium_st_pro
                ordered_building_list = [
                    resources_probability['metal_mine'],
                    resources_probability['crystal_mine'],
                    resources_probability['deuterium_mine'],
                    resources_probability['solar_energy'],
                    resources_probability['fusion_energy'],
                    resources_probability['metal_storage'],
                    resources_probability['crystal_storage'],
                    resources_probability['deuterium_storage']
                ]

                prob = np.array(ordered_building_list)
                action_prob_numbers = prob.cumsum()
                result = np.where(action_prob_numbers > number)
                action_code = result[0][0]

            action = self.resources_action_map[action_code]

            if not self._is_posible(empire, planet_id, action_code):
                print("Action programmed with code " + str(action_code))
                self.programmed_action_code[planet_id] = action_code
                action = None

        return action


# buildings.metal_mine
# buildings.crystal_mine
# buildings.deuterium_mine
# buildings.solar_plant
# buildings.fusion_plant
# buildings.solar_satellite(int)
# buildings.crawler(int)
# buildings.metal_storage
# buildings.crystal_storage
# buildings.deuterium_storage
