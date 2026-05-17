from .base import MongoRepository
from ..core.collections import CollectionName


relationships_repository = MongoRepository(CollectionName.RELATIONSHIPS)
