"""Логика игры в города для бота"""


class Cities_Session:
    def __init__(self):
        self.cities = self._load_cities_from_file()
        self.used_cities = []

    def _load_cities_from_file():
        with open("txt-cities-russia.txt", "r", encoding="utf-8") as input_file:
            cities = {}
            cities.setdefault([])
            for line in input_file:
                city = line.strip().capitalize()
                cities[city[0]].append(city)
        return cities

    def answer(city: str) -> str:
        if city in self.used_cities:
            return "Этот город мы уже называли. Назовите другой."
        if city not in self.cities.values():
            return "Я не знаю в России такого города. Назовите город в России."
        # TODO: Добавить проверку на исчерпание букв в словаре
        # TODO: Добавить логику выбора города для ответа
        return city
