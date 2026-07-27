from .base import MongoRepository
from core.collections import CollectionName


artists_repository = MongoRepository(CollectionName.ARTISTS)
