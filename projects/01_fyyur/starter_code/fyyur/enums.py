from enum import IntEnum


class ChoiceEnum(IntEnum):
    __labels__ = {}

    @property
    def label(self):
        return self.__labels__.get(self.value, self.name.replace('_', ' ').title())

    @classmethod
    def choices(cls):
        return [(choice.value, choice.label) for choice in cls]


class State(ChoiceEnum):
    AL = 1
    AK = 2
    AZ = 3
    AR = 4
    CA = 5
    CO = 6
    CT = 7
    DE = 8
    DC = 9
    FL = 10
    GA = 11
    HI = 12
    ID = 13
    IL = 14
    IN = 15
    IA = 16
    KS = 17
    KY = 18
    LA = 19
    ME = 20
    MT = 21
    NE = 22
    NV = 23
    NH = 24
    NJ = 25
    NM = 26
    NY = 27
    NC = 28
    ND = 29
    OH = 30
    OK = 31
    OR = 32
    MD = 33
    MA = 34
    MI = 35
    MN = 36
    MS = 37
    MO = 38
    PA = 39
    RI = 40
    SC = 41
    SD = 42
    TN = 43
    TX = 44
    UT = 45
    VT = 46
    VA = 47
    WA = 48
    WV = 49
    WI = 50
    WY = 51

    @property
    def label(self):
        return self.name


class Genre(ChoiceEnum):
    ALTERNATIVE = 1
    BLUES = 2
    CLASSICAL = 3
    COUNTRY = 4
    ELECTRONIC = 5
    FOLK = 6
    FUNK = 7
    HIP_HOP = 8
    HEAVY_METAL = 9
    INSTRUMENTAL = 10
    JAZZ = 11
    MUSICAL_THEATRE = 12
    POP = 13
    PUNK = 14
    RNB = 15
    REGGAE = 16
    ROCK_N_ROLL = 17
    SOUL = 18
    OTHER = 19

    __labels__ = {
        HIP_HOP: 'Hip-Hop',
        ROCK_N_ROLL: 'Rock & Roll'
    }

