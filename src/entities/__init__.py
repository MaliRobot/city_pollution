from sqlalchemy.orm import relationship

from db.models.base import mapper_registry
from db.models.city import city_table
from db.models.pollution import pollution_table
from entities.city import City
from entities.pollution import Pollution

city_entity_mapper = mapper_registry.map_imperatively(
    City,
    city_table,
)

pollution_entity_mapper = mapper_registry.map_imperatively(
    Pollution,
    pollution_table,
    properties={"city": relationship(City)},
)
