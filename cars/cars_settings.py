from enum import Enum


class CarYearEnum(Enum):
    MIN_YEAR = 2008
    MAX_YEAR = 2024

    @classmethod
    def year_range(cls):
        return list(range(cls.MIN_YEAR.value, cls.MAX_YEAR.value + 1))


class CarEngVEnum(Enum):
    MIN_ENG_V = 0
    MAX_ENG_V = 6000

    @classmethod
    def eng_v_range(cls):
        return list(range(cls.MIN_ENG_V.value, cls.MAX_ENG_V.value + 1, 1000))
