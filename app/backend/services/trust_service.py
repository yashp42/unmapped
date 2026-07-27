import asyncio
from database.connection import get_database

async def contributor_trust(user_id: str) -> dict:
    """Explainable trust signals; never used as an opaque ranking algorithm."""
    db = get_database()
    lore, theories, connections, reports = await asyncio.gather(
        db.lore.count_documents({"user_id": user_id, "status": "published"}),
        db.theories.count_documents({"user_id": user_id, "status": "published"}),
        db.connection_submissions.count_documents({"author_id": user_id, "status": "approved"}),
        db.reports.count_documents({"reporter_id": user_id, "status": "open"}),
    )
    score = lore * 3 + theories * 3 + connections * 2 - reports
    if score >= 40: level = "trusted contributor"
    elif score >= 12: level = "contributor"
    elif score >= 3: level = "emerging contributor"
    else: level = "reader"
    return {"level": level, "score": max(score, 0), "published_lore": lore, "published_theories": theories, "approved_connections": connections, "open_reports": reports}
