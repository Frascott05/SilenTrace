def is_external_ip(ip: str) -> bool:
    if not ip:
        return False

    return not ip.startswith((
        "127.",
        "10.",
        "172.16.",
        "192.168"
    ))
