# ./AutoUploader/Enums.py
from enum import Enum, unique

@unique
class StageTypes(Enum):
    Campaign = 0
    KingsTower = 1
    LightbearerTower = 2
    MaulerTower = 3
    WilderTower = 4
    GravebearerTower = 5
    CelestialTower = 6
    HypogeanTower = 7


ImageTypes = ['BattleStatistics', 'HeroInfo']