# Следующие 3 класса болваночные для инпута-аутпута
class InputPersData:
    def __init__(self, data):
        self.data = data


class InputPlacesData:
    def __init__(self, data):
        self.data = data


class OutputPlaces:
    def __init__(self, data):
        self.data = data


# Основной класс рекомендательной системы, в котором реализуется подсчет метрики для тегов
class RecommendationSystem:
    def countLikelihood(self, pers_data: InputPersData, places_data: InputPlacesData) -> float:
        pass


# Подкласс рекомендательной системы расширенный на дпоолнительное использование геопозиции
class RSWithGeo(RecommendationSystem):
    def __init__(self, pers_data: InputPersData, places_data: InputPlacesData):
        super().__init__(pers_data, places_data)
        self.geo = None

    def countGeoLikelihood(self, places_data: InputPlacesData) -> float:
        pass

    def countLikelihood(self, pers_data: InputPersData, places_data: InputPlacesData) -> float:
        tags_likelihood = super().countLikelihood(pers_data)
        geo_likelihood = self.countGeoLikelihood(places_data)
        return 0.5



