import re
if not re.match(r'^[\w-]+$', toolUser or ''):
    return Response(json.dumps({"message": "Invalid user"}), status=400, mimetype="application/json")
