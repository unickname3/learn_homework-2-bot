"""Логика игры в города для бота"""


class CitiesSession:
    def __init__(self):
        self.cities_dict = {}
        self.used_cities = set()
        self.lack_letters = set()
        self.all_cities = set()
        self.letter_for_user = ""
        self._load_cities_from_file()

    def _load_cities_from_file(self):
        with open("txt-cities-russia.txt", "r", encoding="utf-8") as input_file:
            cities = {}
            for line in input_file:
                city = line.strip().capitalize()
                cities.setdefault(city[0], set())
                cities[city[0]].add(city)

        self.lack_letters = (
            set([chr(k) for k in range(ord("А"), ord("Я") + 1)]) - cities.keys()
        )
        print(self.lack_letters)
        self.cities_dict = cities
        self.all_cities = set.union(*cities.values())

    def answer(self, user_city: str) -> str:
        # TODO: Порефакторить этот метод
        user_city = user_city.capitalize()

        if user_city in self.used_cities:
            return "Этот город мы уже называли. Назовите другой."

        if user_city not in self.all_cities:
            return "Я не знаю такого города в России. Назовите другой."

        if self.letter_for_user and user_city[0] != self.letter_for_user:
            return f"Вы должны назвать город на букву {self.letter_for_user}"

        self.used_cities.add(user_city)

        exhaust = []
        for letter in user_city.upper()[::-1]:
            if letter in self.lack_letters:
                exhaust.append(letter)
                continue

            for city in self.cities_dict[letter]:
                if city not in self.used_cities:
                    print(self.used_cities)
                    answer = []
                    bot_city = city
                    self.used_cities.add(bot_city)
                    self.letter_for_user = [
                        k for k in bot_city.upper() if k not in self.lack_letters
                    ][-1].upper()

                    if exhaust:
                        answer.append(
                            f"Нет доступных городов на буквы {', '.join(exhaust)}."
                        )
                    answer.append(f"Мне на {letter}: {bot_city}.")
                    answer.append(f"Вам на {self.letter_for_user}.")

                    return "\n".join(answer)

            exhaust.append(letter)
            self.lack_letters.add(letter)

        return f"К сожалению, нет доступных городов на буквы {', '.join(exhaust)}"


if __name__ == "__main__":
    cities_game = CitiesSession()
    test_cities = ["4234234", "ььыъ", "Москва", "Коломна", "Астрахань", "Краснодар"]
    for city in test_cities:
        print(f"Me > {city}")
        print(f"Bot> {cities_game.answer(city)}")
