from .base import MongoRepository
from ..core.collections import CollectionName


contributors_repository = MongoRepository(CollectionName.CONTRIBUTORS)
