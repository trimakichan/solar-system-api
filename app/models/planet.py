class Planet():
    def __init__(self, id, name, description, distance_from_sun):
        self.id = id
        self.name = name
        self.description = description
        self.distance_from_sun = distance_from_sun


PLANETS = [
    Planet(1, "Mercury", "Smallest planet, closest to the Sun", 123456),
    Planet(2, "Earth", "Our home", 654321)
]