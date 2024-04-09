from sqlalchemy.orm import relationship

from data_project.db.models.base import mapper_registry
from data_project.db.models.city import city_table
from data_project.db.models.pollution import pollution_table
from data_project.entities.city import City
from data_project.entities.pollution import Pollution

city_entity_mapper = mapper_registry.map_imperatively(
    City,
    city_table,
)

pollution_entity_mapper = mapper_registry.map_imperatively(
    Pollution,
    pollution_table,
    properties={"city": relationship(City)},
)
