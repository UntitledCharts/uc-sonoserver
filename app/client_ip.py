import ipaddress

from starlette.requests import HTTPConnection

FALLBACK_HEADERS = ("x-real-ip", "cf-connecting-ip", "true-client-ip")


def _clean(value: str) -> str | None:
    """Normalize an address from a header.

    Args:
        value: Raw header value.

    Returns:
        str | None: The address, or None when it isn't an IP address.
    """
    candidate = value.strip().strip('"')
    if candidate.startswith("[") and "]" in candidate:
        candidate = candidate[1 : candidate.index("]")]
    elif candidate.count(":") == 1 and "." in candidate:
        candidate = candidate.split(":", 1)[0]
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return None


def _from_forwarded(value: str, trusted_proxies: int) -> str | None:
    """Read the client from an RFC 7239 Forwarded header.

    Args:
        value: Header value.
        trusted_proxies: Proxies in front of the app.

    Returns:
        str | None: The address, or None.
    """
    addresses = []
    for element in value.split(","):
        for pair in element.split(";"):
            name, _, raw = pair.strip().partition("=")
            if name.lower() == "for":
                addresses.append(raw)
    if len(addresses) < trusted_proxies or trusted_proxies <= 0:
        return None
    return _clean(addresses[-trusted_proxies])


def client_ip(connection: HTTPConnection, trusted_proxies: int) -> str | None:
    """Find the real client address behind the configured proxies.

    Args:
        connection: Current request.
        trusted_proxies: Proxies in front of the app.

    Returns:
        str | None: The client address, or None when none could be read.
    """
    forwarded_for = connection.headers.get("x-forwarded-for")
    if forwarded_for and trusted_proxies > 0:
        entries = [entry for entry in forwarded_for.split(",") if entry.strip()]
        if len(entries) >= trusted_proxies:
            address = _clean(entries[-trusted_proxies])
            if address:
                return address
    for header in FALLBACK_HEADERS:
        value = connection.headers.get(header)
        if value:
            address = _clean(value)
            if address:
                return address
    forwarded = connection.headers.get("forwarded")
    if forwarded:
        address = _from_forwarded(forwarded, trusted_proxies)
        if address:
            return address
    if connection.client is not None:
        return _clean(connection.client.host)
    return None
