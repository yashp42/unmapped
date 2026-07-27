from .base import MongoRepository
from ..core.collections import CollectionName


theories_repository = MongoRepository(CollectionName.THEORIES)
