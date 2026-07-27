from .base import MongoRepository
from ..core.collections import CollectionName


tracks_repository = MongoRepository(CollectionName.TRACKS)
