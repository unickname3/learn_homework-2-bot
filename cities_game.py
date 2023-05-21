"""Логика игры в города для бота"""


class Cities_Sesssion:
    def __init__(self, player_id):
        self.player_id = player_id
        self.cities = self._load_cities_from_file()
        self.used_cities = set()

    def _load_cities_from_file():
        with open("txt-cities-russia.txt", "r", encoding="utf-8") as input_file:
            cities = {}
            cities.setdefault([])
            for line in input_file:
                city = line.strip().capitalize()
                cities[city[0]].append(city)
        return cities
