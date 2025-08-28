from enum import Enum
import struct

class TileCategory:
    name: str
    color: tuple

class TileSpecs(Enum):
    """
    Reference: https://rainworldmodding.miraheze.org/wiki/Creating_Custom_Tiles_and_Props#Specs
    """
    Arbitrary   = -1
    Air         = 0
    Solid       = 1
    TRSlope     = 2
    TLSlope     = 3
    BRSlope     = 4
    BLSlope     = 5
    Platform    = 6
    #Shortcut   = 7  <- might crash editor
    #Unused     = 8  <- might crash editor
    Glass       = 9

class TileTypes(Enum):
    """
    Reference: https://rainworldmodding.miraheze.org/wiki/Creating_Custom_Tiles_and_Props#Tile_types
    """
    Normal                      = "voxelStruct"
    Box                         = "box"
    RockType                    = "voxelStructRockType"
    RandomDisplacerH            = "voxelStructRandomDisplaceHorizontal"
    RandomDisplacerV            = "voxelStructRandomDisplaceVertical"
    SandType                    = "voxelStructSandType"

class TileTags(Enum):
    """
    Reference: https://rainworldmodding.miraheze.org/wiki/Creating_Custom_Tiles_and_Props#Possible_tile_tags
    """
    NotTrashProp                = "notTrashProp"
    NotProp                     = "notProp"
    NonSolid                    = "nonSolid"
    DrawLast                    = "drawLast"
    BigSign                     = "Big Sign"
    SmallAsianSign              = "Small Asian Sign"
    SmallAsianSignWall          = "small asian sign on wall"
    BigWesternSign              = "Big Western Sign"
    BigWesternSignTilted        = "Big Western Sign Tilted"
    LargerSign                  = "LargerSign"
    BigWheel                    = "Big Wheel"
    ChainHolder                 = "Chain Holder"
    FanBlade                    = "fanBlade"
    Harvester                   = "harvester"
    TempleFloor                 = "Temple Floor"
    RandomCords                 = "randomCords"
    EffectColorA                = "effectColorA"
    EffectColorB                = "effectColorB"
    BigSignB                    = "Big Sign B"
    BigWesternSignB             = "Big Western Sign B"
    BigWesternSignTiltedB       = "Big Western Sign Tilted B"
    SmallAsianSignB             = "Small Asian Sign B"
    SmallAsianSignWallB         = "small asian sign on wall B"
    SmallAsianSignStation       = "Small Asian Sign Station"
    SmallAsianSignWallStation   = "Small Asian Sign On Wall Station"
    SmallAsianSignStationB      = "Small Asian Sign Station B"
    SmallAsianSignWallStationB  = "Small Asian Sign On Wall Station B"
    LargerSignB                 = "Larger Sign B"
    StationLargerSign           = "Station Larger Sign"
    StationLargerSignB          = "Station Larger Sign B"
    StationLamp                 = "Station Lamp"
    LumiaireH                   = "LumiaireH"
    NotMegaTrashProp            = "notMegaTrashProp"
    NotTile                     = "notTile"
    Ramp                        = "ramp"
    Glass                       = "glass"

class Tile:
    def __init__(self):
        self.category: TileCategory = TileCategory()
        self.name: str = ""
        self.size: tuple[int, int] = (0, 0)
        self.specs: list[TileSpecs] = []
        self.specs2: list[TileSpecs] | None = None
        self.type_: TileTypes = TileTypes.Normal
        self.bufferTiles: int = 0
        self.random: int = 0
        self.pointPos = 0
        self.repeatLayers: list[int] | None = None
        self.tags: list[TileTags] = []
    
    def __repr__(self):
        return f"<Tiles.Tile name='{self.name}' category='{self.category.name}' type='{self.type_.value}' at {hex(id(self))}>"
    
    def __str__(self):
        return f"{self.category.name}: {self.name}"
    
    def serialize(self):
        return {
            "category": {"name": self.category.name, "color": self.category.color},
            "name": self.name,
            "size": self.size,
            "specs": [x.value for x in self.specs],
            "specs2": [x.value for x in self.specs2] if self.specs2 != None else 0,
            "type": self.type_.value,
            "bufferTiles": self.bufferTiles,
            "random": self.random,
            "pointPos": self.pointPos,
            "repeatLayers": self.repeatLayers,
            "tags": [x.value if isinstance(x, TileTags) else x for x in self.tags]
        }