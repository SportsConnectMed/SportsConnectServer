import enum


class SkillLevel(
    str,
    enum.Enum,
):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
