from sqlalchemy.orm import relationship

from app.db.models.base import mapper_registry
from app.db.models.city import city_table
from app.db.models.pollution import pollution_table
from app.entities.city import City
from app.entities.pollution import Pollution

city_entity_mapper = mapper_registry.map_imperatively(
    City,
    city_table,
)

pollution_entity_mapper = mapper_registry.map_imperatively(
    Pollution,
    pollution_table,
    properties={"city": relationship(City)},
)
