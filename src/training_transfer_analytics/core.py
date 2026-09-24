def _unit_interval(value: float, name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")


def transfer_index(self_rating, manager_rating, behavior_score, opportunity=1.0):
    """Combine three evidence sources and scale by opportunity to perform."""
    for name, value in (
        ("self_rating", self_rating),
        ("manager_rating", manager_rating),
        ("behavior_score", behavior_score),
        ("opportunity", opportunity),
    ):
        _unit_interval(value, name)
    base = 0.25 * self_rating + 0.35 * manager_rating + 0.40 * behavior_score
    return base * opportunity


def retention_adjusted(index, days, half_life=60):
    """Apply exponential half life decay to an observed transfer index."""
    _unit_interval(index, "index")
    if days < 0:
        raise ValueError("days must be non-negative")
    if half_life <= 0:
        raise ValueError("half_life must be positive")
    return index * (0.5 ** (days / half_life))


def barrier_flags(manager_support, opportunity, tool_access):
    """Return simple contextual barriers below the 0.5 review threshold."""
    for name, value in (
        ("manager_support", manager_support),
        ("opportunity", opportunity),
        ("tool_access", tool_access),
    ):
        _unit_interval(value, name)
    flags = []
    if manager_support < 0.5:
        flags.append("manager_support")
    if opportunity < 0.5:
        flags.append("opportunity_to_perform")
    if tool_access < 0.5:
        flags.append("tool_access")
    return flags
