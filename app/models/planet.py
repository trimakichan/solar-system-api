class Planet():
    def __init__(self, id, name, description, distance_from_sun):
        self.id = id
        self.name = name
        self.description = description
        self.distance_from_sun = distance_from_sun

# They are exactly the same — 57_910_000 and 57910000 — but the first one is easier to read. 
planets = [
    Planet(1, "Mercury", "Smallest planet, closest to the Sun", 57_910_000),
    Planet(2, "Earth", "Our beautiful home", 149_600_000),
    Planet(3, "Venus", "Second planet, covered with thick clouds of sulfuric acid", 108_200_000),
    Planet(4, "Jupiter", "Largest planet with a massive storm", 778_500_000)
]
