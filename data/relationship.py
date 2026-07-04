RELATIONSHIP_LIMITS = {
    "trust": 100,
    "closeness": 100,
    "attachment": 100,
}

relationships = {
    "trust": 60,
    "closeness": 65,
    "attachment": 55,
}


def _validate_relationship(name):
    if name not in relationships:
        raise ValueError(f"Unknown relationship: {name}")


def _clamp_relationship(name, value):
    return max(0, min(RELATIONSHIP_LIMITS[name], value))


def increase_relationship(name, amount):
    _validate_relationship(name)
    amount = max(0, amount)
    relationships[name] = _clamp_relationship(
        name,
        relationships[name] + amount
    )
    return relationships[name]


def decrease_relationship(name, amount):
    _validate_relationship(name)
    amount = max(0, amount)
    relationships[name] = _clamp_relationship(
        name,
        relationships[name] - amount
    )
    return relationships[name]


def get_relationship(name):
    _validate_relationship(name)
    return relationships[name]


def reset_relationship():
    for name in relationships:
        relationships[name] = 0
    return relationships


def get_relationship_level():
    total = (
        relationships["trust"]
        + relationships["closeness"]
        + relationships["attachment"]
    )
    average = total / 3

    if average <= 19:
        return "STRANGER"

    if average <= 39:
        return "ACQUAINTANCE"

    if average <= 59:
        return "FRIEND"

    if average <= 79:
        return "CLOSE"

    return "FAMILY"