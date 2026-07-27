"""Public music metadata adapter.

Uses Apple's unauthenticated Search API for canonical store metadata/artwork and
Wikimedia page summaries for artist context.  The adapter is deliberately kept
server-side so provider details, caching and future provider changes do not leak
into the interface.
"""
from __future__ import annotations

import asyncio
from difflib import SequenceMatcher
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

import requests

from ..database.connection import get_database
from .catalog_identity import persist_catalog_entities

ITUNES_URL = "https://itunes.apple.com/search"
MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2/release-group"
WIKI_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"
HEADERS = {"User-Agent": "Unmapped/0.3 (music-culture prototype)"}
CACHE_FOR = timedelta(days=7)
EMPTY_CACHE_FOR = timedelta(minutes=10)


def _hi_res(url: str | None) -> str | None:
    """Apple search returns a small rendition; request its documented CDN size."""
    return url.replace("100x100bb", "1200x1200bb") if url else None


async def _cached(key: str, resolver):
    cache = get_database().catalog_cache
    hit = await cache.find_one({"_id": key})
    now = datetime.now(timezone.utc)
    if hit and hit.get("expires_at", now) > now:
        return hit["payload"]
    # Provider calls are blocking HTTP. Offload them so a slow catalogue never
    # stalls unrelated API requests on FastAPI's event loop.
    payload = await asyncio.to_thread(resolver)
    await cache.update_one(
        {"_id": key},
        {"$set": {"payload": payload, "expires_at": now + (CACHE_FOR if payload else EMPTY_CACHE_FOR)}},
        upsert=True,
    )
    return payload


def _itunes(term: str, entity: str) -> dict | None:
    try:
        response = requests.get(ITUNES_URL, params={"term": term, "entity": entity, "country": "US", "limit": 5}, headers=HEADERS, timeout=5)
        response.raise_for_status()
        results = response.json().get("results") or []
        if not results:
            return None
        query = term.lower()
        def score(item: dict) -> float:
            title = item.get("trackName") or item.get("collectionName") or ""
            artist = item.get("artistName") or ""
            return max(SequenceMatcher(None, query, f"{artist} {title}".lower()).ratio(), SequenceMatcher(None, query, title.lower()).ratio() * 0.85)
        best = max(results, key=score)
        best["metadata_confidence"] = round(score(best), 3)
        return best
    except (requests.RequestException, ValueError):
        return None


def _itunes_many(term: str) -> list[dict]:
    try:
        response = requests.get(ITUNES_URL, params={"term": term, "media": "music", "entity": "song", "country": "US", "limit": 25}, headers=HEADERS, timeout=7)
        response.raise_for_status()
        return response.json().get("results") or []
    except (requests.RequestException, ValueError):
        return []


def _musicbrainz_album(title: str, artist: str) -> dict | None:
    """Open-data fallback for releases missing from the commercial catalogue."""
    try:
        response = requests.get(MUSICBRAINZ_URL, params={"query": f'releasegroup:"{title}" AND artist:"{artist}"', "fmt": "json", "limit": 1}, headers=HEADERS, timeout=7)
        response.raise_for_status()
        group = (response.json().get("release-groups") or [None])[0]
        if not group:
            return None
        return {"artworkUrl100": f"https://coverartarchive.org/release-group/{group['id']}/front-1200", "collectionViewUrl": f"https://musicbrainz.org/release-group/{group['id']}", "releaseDate": group.get("first-release-date"), "metadata_provider": "MusicBrainz / Cover Art Archive"}
    except (requests.RequestException, ValueError, KeyError):
        return None


def _wiki(name: str) -> dict:
    try:
        response = requests.get(f"{WIKI_URL}{quote(name, safe='')}", headers=HEADERS, timeout=5)
        if response.status_code != 200:
            return {}
        data = response.json()
        return {"bio": data.get("extract"), "portrait_url": data.get("thumbnail", {}).get("source"), "wiki_url": data.get("content_urls", {}).get("desktop", {}).get("page")}
    except (requests.RequestException, ValueError):
        return {}


async def enrich_album(album: dict, artist_name: str | None = None) -> dict:
    artist_name = artist_name or album.get("artist_name") or ""
    key = f"album:{artist_name}:{album.get('title', '')}".lower()
    item = await _cached(key, lambda: _itunes(f"{artist_name} {album.get('title', '')}", "album") or _musicbrainz_album(album.get("title", ""), artist_name) or {})
    return {**album, "artist_name": artist_name, "artwork_url": _hi_res(item.get("artworkUrl100")), "artwork_source": item.get("metadata_provider") or ("Apple Music catalogue" if item else None), "metadata_confidence": item.get("metadata_confidence", 0.7), "external_url": item.get("collectionViewUrl"), "release_date": item.get("releaseDate")}


async def enrich_track(track: dict, artist_name: str | None = None, album: dict | None = None) -> dict:
    artist_name = artist_name or track.get("artist_name") or ""
    album_title = (album or {}).get("title", "")
    key = f"track:{artist_name}:{track.get('title', '')}:{album_title}".lower()
    item = await _cached(key, lambda: _itunes(f"{artist_name} {track.get('title', '')}", "song") or {})
    return {**track, "artist_name": artist_name, "artwork_url": _hi_res(item.get("artworkUrl100")), "artwork_source": "Apple Music catalogue" if item else None, "metadata_confidence": item.get("metadata_confidence", 0.7), "external_url": item.get("trackViewUrl"), "preview_url": item.get("previewUrl"), "album_title": item.get("collectionName") or album_title}


async def enrich_artist(artist: dict) -> dict:
    name = artist.get("name", "")
    key = f"artist:{name}".lower()
    context = await _cached(key, lambda: _wiki(name))
    return {**artist, **context}


async def explore_catalog() -> dict:
    db = get_database()
    artists = await db.artists.find({}, {"_id": 0}).sort("name", 1).to_list(length=100)
    by_id = {artist["id"]: artist for artist in artists}
    albums = await db.albums.find({}, {"_id": 0}).sort("year", -1).to_list(length=100)
    tracks = await db.tracks.find({}, {"_id": 0}).sort("title", 1).to_list(length=200)
    enriched_artists = await asyncio.gather(*(enrich_artist(artist) for artist in artists))
    enriched_albums = await asyncio.gather(*(enrich_album(album, by_id.get(album.get("artist_id"), {}).get("name")) for album in albums))
    by_album = {album["id"]: album for album in albums}
    enriched_tracks = await asyncio.gather(*(enrich_track(track, by_id.get(track.get("artist_id"), {}).get("name"), by_album.get(track.get("album_id"))) for track in tracks))
    return {"albums": list(enriched_albums), "artists": list(enriched_artists), "tracks": list(enriched_tracks)}


async def live_search(term: str) -> dict:
    """Provider-backed discovery results, shaped like the curated archive."""
    results = await _cached(f"search:{term.lower()}", lambda: _itunes_many(term))
    tracks, albums, artists = [], [], []
    seen_albums, seen_artists = set(), set()
    for item in results:
        artist_name = item.get("artistName", "Unknown artist")
        track_title = item.get("trackName")
        album_title = item.get("collectionName")
        artwork = _hi_res(item.get("artworkUrl100"))
        if track_title:
            tracks.append({"id": f"external-track-{item.get('trackId')}", "title": track_title, "artist_name": artist_name, "album_title": album_title, "duration": "", "artwork_url": artwork, "external_url": item.get("trackViewUrl")})
        album_key = item.get("collectionId")
        if album_title and album_key not in seen_albums:
            seen_albums.add(album_key)
            albums.append({"id": f"external-album-{album_key}", "title": album_title, "artist_name": artist_name, "year": (item.get("releaseDate") or "")[:4], "universe_tagline": "", "artwork_url": artwork, "external_url": item.get("collectionViewUrl")})
        artist_key = item.get("artistId")
        if artist_key not in seen_artists:
            seen_artists.add(artist_key)
            artists.append({"id": f"external-artist-{artist_key}", "name": artist_name, "tagline": "", "scene": item.get("primaryGenreName", "music"), "era": "", "portrait_url": None, "external_url": item.get("artistViewUrl")})
    await asyncio.gather(persist_catalog_entities(tracks, "track"), persist_catalog_entities(albums, "album"), persist_catalog_entities(artists, "artist"))
    return {"tracks": tracks, "albums": albums, "artists": artists}
