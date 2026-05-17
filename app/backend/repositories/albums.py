from .base import MongoRepository
from ..core.collections import CollectionName


albums_repository = MongoRepository(CollectionName.ALBUMS)
