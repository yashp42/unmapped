from ..config import settings
from .connection import db


async def create_indexes():
    # Users
    await db.users.create_index("email", unique=True)
    await db.users.create_index("handle", unique=True)

    # Artists
    await db.artists.create_index("id", unique=True)
    await db.artists.create_index([("name", "text")], name="artists_text")

    # Albums
    await db.albums.create_index("id", unique=True)
    await db.albums.create_index([("title", "text"), ("artist_name", "text")], name="albums_text")

    # Tracks
    await db.tracks.create_index("id", unique=True)
    await db.tracks.create_index([("title", "text"), ("artist_name", "text")], name="tracks_text")

    # Vibes
    await db.vibes.create_index("id", unique=True)
    await db.vibes.create_index([("name", "text"), ("felt_state", "text")], name="vibes_text")

    # Lore
    await db.lore.create_index("id", unique=True)
    await db.lore.create_index([("title", "text"), ("excerpt", "text"), ("content", "text")], name="lore_text")

    # Theories
    await db.theories.create_index("id", unique=True)
    await db.theories.create_index([("title", "text"), ("abstract", "text")], name="theories_text")

    # Contributors
    await db.contributors.create_index("id", unique=True)
    await db.contributors.create_index("handle", unique=True)

    # Collections
    await db.collections.create_index("id", unique=True)
    await db.collections.create_index([("owner_id", 1)])

    # Graph / archive metadata
    await db.connections.create_index([("source", 1), ("target", 1)])
    await db.sample_chains.create_index("track_id")
    await db.transitions.create_index("album_id")
    await db.lore.create_index("album_id")
    await db.lore.create_index("track_id")
    await db.lore.create_index("author")
    await db.lore.create_index("user_id")
    await db.theories.create_index("album_id")
    await db.theories.create_index("author")
    await db.theories.create_index("user_id")
    await db.tracks.create_index("album_id")

    # Comments
    await db.comments.create_index([("target_type", 1), ("target_id", 1), ("created_at", 1)])
    await db.comments.create_index("user_id")
