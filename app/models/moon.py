from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .planet import Planet

class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    size: Mapped[int]
    description: Mapped[str]
    color: Mapped[str]
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="moons")


    def to_dict(self):
        return {
            "id": self.id,
            "size": self.size,
            "description": self.description,
            "color": self.color,
            "planet_id": self.planet_id
        }
    
    @classmethod
    def from_dict(cls, moon_data):
        new_moon = cls(size=moon_data["size"],
                        description=moon_data["description"],
                        color=moon_data["color"],
                        planet_id=moon_data.get("planet_id"))

        
        return new_moon