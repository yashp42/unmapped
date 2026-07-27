def catalog_id(kind: str, provider: str, provider_id: str | int | None) -> str:
    return f"{provider}-{kind}-{provider_id}"
