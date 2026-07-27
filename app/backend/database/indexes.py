from backend.config import settings
from database.connection import get_database


async def create_indexes():
    # Users
    db = get_database()
    users_collection = db["users"]
    await users_collection.create_index("email", unique=True)
    await users_collection.create_index("handle", unique=True)
    await users_collection.create_index("role")

    # Artists
    await get_database().artists.create_index("id", unique=True)
    await get_database().artists.create_index([("name", "text")], name="artists_text")

    # Albums
    await get_database().albums.create_index("id", unique=True)
    await get_database().albums.create_index([("title", "text"), ("artist_name", "text")], name="albums_text")

    # Tracks
    await get_database().tracks.create_index("id", unique=True)
    await get_database().tracks.create_index([("title", "text"), ("artist_name", "text")], name="tracks_text")

    # Lore
    await get_database().lore.create_index("id", unique=True)
    await get_database().lore.create_index([("title", "text"), ("excerpt", "text"), ("content", "text")], name="lore_text")

    # Theories
    await get_database().theories.create_index("id", unique=True)
    await get_database().theories.create_index([("title", "text"), ("abstract", "text")], name="theories_text")

    # Contributors
    await get_database().contributors.create_index("id", unique=True)
    await get_database().contributors.create_index("handle", unique=True)

    # Collections
    await get_database().collections.create_index("id", unique=True)
    await get_database().collections.create_index([("owner_id", 1)])

    # Graph / archive metadata
    await get_database().connections.create_index([("source", 1), ("target", 1)])
    await get_database().connections.create_index("type")
    await get_database().relationships.create_index([("source_id", 1), ("target_id", 1), ("type", 1)])
    await get_database().relationships.create_index("source_type")
    await get_database().relationships.create_index("target_type")
    await get_database().sample_chains.create_index("track_id")
    await get_database().transitions.create_index("album_id")
    await get_database().lore.create_index("album_id")
    await get_database().lore.create_index("track_id")
    await get_database().lore.create_index("author")
    await get_database().lore.create_index("user_id")
    await get_database().theories.create_index("album_id")
    await get_database().theories.create_index("author")
    await get_database().theories.create_index("user_id")
    await get_database().tracks.create_index("album_id")

    # Comments
    await get_database().comments.create_index([("target_type", 1), ("target_id", 1), ("created_at", 1)])
    await get_database().comments.create_index("user_id")

    # Annotations
    await get_database().annotations.create_index([("target_type", 1), ("target_id", 1), ("created_at", 1)])
    await get_database().annotations.create_index("user_id")
    await get_database().annotations.create_index("status")
    await get_database().reactions.create_index([("target_type", 1), ("target_id", 1), ("user_id", 1), ("kind", 1)], unique=True)
    await get_database().catalog_cache.create_index("expires_at", expireAfterSeconds=0)
    await get_database().catalog_entities.create_index("id", unique=True)
    await get_database().catalog_entities.create_index([("kind", 1), ("title", "text"), ("artist_name", "text")], name="catalog_entities_search")
    await get_database().submission_events.create_index([("user_id", 1), ("kind", 1), ("created_at", 1)])
    await get_database().submission_events.create_index("expires_at", expireAfterSeconds=0)
    await get_database().connection_submissions.create_index([("status", 1), ("created_at", -1)])
    await get_database().reports.create_index([("target_type", 1), ("target_id", 1), ("reporter_id", 1)], unique=True)
    await get_database().lore.create_index([("status", 1), ("created_at", -1)])
    await get_database().theories.create_index([("status", 1), ("created_at", -1)])
    await get_database().audit_events.create_index([("target_type", 1), ("target_id", 1), ("created_at", -1)])
    await get_database().content_revisions.create_index([("content_type", 1), ("content_id", 1), ("created_at", -1)])
