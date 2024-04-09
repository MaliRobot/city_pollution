from sqlalchemy.orm import relationship

from city_pollution.db.models.base import mapper_registry
from city_pollution.db.models.city import city_table
from city_pollution.db.models.pollution import pollution_table
from city_pollution.entities.city import City
from city_pollution.entities.pollution import Pollution

city_entity_mapper = mapper_registry.map_imperatively(
    City,
    city_table,
)

pollution_entity_mapper = mapper_registry.map_imperatively(
    Pollution,
    pollution_table,
    properties={"city": relationship(City)},
)
