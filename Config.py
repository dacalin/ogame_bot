import json



class Config:
    def __init__(self, path: str):
        self.path = path
        file = open(path)
        self.config_data = json.load(file)

    def user(self) -> str:
        return self.config_data['user']

    def password(self) -> str:
        return self.config_data['password']

    def universe(self) -> str:
        return self.config_data['universe']

    def language(self) -> str:
        return self.config_data['language']

    def planets(self) -> list:

        planets_ids = []
        for planet in self.config_data['planets']:
            planets_ids.append(planet['id'])

        return planets_ids

    def _planet_config(self, planet_id):
        planet_config = None

        for planet in self.config_data['planets']:
            if planet['id'] == planet_id:
                planet_config = planet
                break

        return planet_config

    def planet_action_type_probabilities(self, planet_id):

        planet_config = self._planet_config(planet_id)

        return planet_config['probabilities']

    def supplies_probabilities(self, planet_id):
        planet_config = self._planet_config(planet_id)

        return planet_config['supplies']['probabilities']


    def min_supplies_resources(self, planet_id):
        planet_config = self._planet_config(planet_id)

        return planet_config['supplies']['minimun']

    def max_supplies_resources(self, planet_id):
        planet_config = self._planet_config(planet_id)

        return planet_config['supplies']['maximun']
