import hashlib  # noqa: F401  (you will need these on day 5)
import hmac  # noqa: F401


def verify_signature(body: bytes, header_value: str | None, secret: str) -> bool:
    """Day 5: validate an HMAC-SHA256 webhook signature.

    Expected header format:  "sha256=<hex digest>"
    The digest is HMAC-SHA256(key=secret, msg=raw request body).

    Hints:
      - return False if the header is missing or has the wrong prefix
      - compute the expected digest with hmac.new(...).hexdigest()
      - compare with hmac.compare_digest, never with ==  (why? think timing attacks)
    """
    raise NotImplementedError("Day 5")
