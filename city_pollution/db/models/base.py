from sqlalchemy.orm import registry

mapper_registry = registry()  # noqa
Base = mapper_registry.generate_base()
