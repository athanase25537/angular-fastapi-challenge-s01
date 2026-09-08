"""Small, dependency-free HS256 JWT helpers used by the API."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, status


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "local-development-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def _encode_part(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _decode_part(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
    }
    header = {"alg": ALGORITHM, "typ": "JWT"}
    signing_input = ".".join(
        (_encode_part(json.dumps(header, separators=(",", ":")).encode()),
         _encode_part(json.dumps(payload, separators=(",", ":")).encode()))
    )
    signature = hmac.new(SECRET_KEY.encode(), signing_input.encode(), hashlib.sha256).digest()
    return f"{signing_input}.{_encode_part(signature)}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        if json.loads(_decode_part(encoded_header)) != {"alg": ALGORITHM, "typ": "JWT"}:
            raise ValueError("Unsupported token header")
        signing_input = f"{encoded_header}.{encoded_payload}"
        expected = hmac.new(SECRET_KEY.encode(), signing_input.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(expected, _decode_part(encoded_signature)):
            raise ValueError("Invalid signature")
        payload = json.loads(_decode_part(encoded_payload))
        if not isinstance(payload.get("sub"), str) or payload.get("exp", 0) <= datetime.now(timezone.utc).timestamp():
            raise ValueError("Expired or malformed token")
        return payload
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError, TypeError):
        raise credentials_exception()


def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
