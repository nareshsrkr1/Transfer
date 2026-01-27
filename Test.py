def sanitize_uid(v):
    return v.strip() if isinstance(v, str) and v.isascii() and 1 <= len(v) <= 50 else None

toolUser = sanitize_uid(request.args.get('userId'))
