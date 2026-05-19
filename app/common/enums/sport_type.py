import enum


class SportType(
    str,
    enum.Enum,
):
    FOOTBALL = "FOOTBALL"
    FUTSAL = "FUTSAL"
    BASKETBALL = "BASKETBALL"
    VOLLEYBALL = "VOLLEYBALL"
    TENNIS = "TENNIS"
    PADEL = "PADEL"
