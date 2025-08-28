import ast, re
import Tiles as tiles

INIT_FILE = "Init.txt"
DEBUG = False

class InitParser:
    def __init__(self, init_data: str|bytes):
        self.data = init_data if isinstance(init_data, str) else init_data.encode("utf-8")
        self.parsed = {}
    
    def parse(self):
        raise NotImplementedError
    
    def encode(self):
        raise NotImplementedError

class GraphicsInitParser(InitParser):
    def __init__(self, init_data: str|bytes):
        super().__init__(init_data)
        self.tiles = []
        self.props = []

    def parse(self, is_tiles: bool = True) -> dict:
        lines = self.data.split("\n")
        currentCategory = None
        property_regex = r"\#([^:\]]+):((?:\s*\[[^\]]*\]|\"[^\"]*\"|point\([^)]+\)|[^,\]]+))(?:, |)"

        for line in lines:
            # Category line
            if line != "" and "-" == line[0]:
                categoryName = f"{(line.split(',')[0])[3:-1]}"
                categoryColor = (
                    int((line.split(',')[1]).strip()[6:]),
                    int((line.split(',')[2]).strip()),
                    int(((line.split(',')[3]).strip())[:-2])
                )
                currentCategory = tiles.TileCategory()
                currentCategory.name = categoryName
                currentCategory.color = categoryColor
                print("Parsing", currentCategory.name + "...") if DEBUG else None
            
            # Tile/Prop properties line
            elif line != "" and "-" != line[0] and isinstance(currentCategory, tiles.TileCategory):
                currentTile = tiles.Tile()
                currentTile.category = currentCategory

                for prprty in re.finditer(property_regex, line, re.M):
                    prprty = (prprty.group()).rstrip(", ")
                    prprty_name = prprty.split(":")[0].lstrip("#")
                    prprty_val = prprty.split(":")[1].strip()

                    match prprty_name:
                        case "nm":
                            currentTile.name = prprty_val.strip('"')
                        case "sz":
                            currentTile.size = (
                                int((prprty_val.split(",")[0])[6:]),
                                int((prprty_val.split(",")[1])[:-1])
                            )
                        case "specs":
                            currentTile.specs = [
                                tiles.TileSpecs(int(i)) for i in prprty_val[1:-1].split(",")
                            ]
                        case "specs2":
                            currentTile.specs2 = None if (prprty_val == "0" or prprty_val == "void") else [
                                tiles.TileSpecs(int(i)) for i in prprty_val[1:-1].split(",")
                            ]
                        case "tp":
                            currentTile.type_ = tiles.TileTypes(prprty_val.strip('"'))
                        case "bfTiles":
                            currentTile.bufferTiles = int(prprty_val)
                        case "rnd":
                            currentTile.random = int(prprty_val)
                        case "ptPos":
                            currentTile.pointPos = 0
                        case "repeatL":
                            currentTile.repeatLayers = [
                                int(i) for i in prprty_val[1:-1].split(",")
                            ]
                        case "tags":
                            for i in prprty_val[1:-1].split(","):
                                try:
                                    if prprty_val != "[]":
                                        currentTile.tags.append(tiles.TileTags(i.strip('" ')))
                                except ValueError:
                                    currentTile.tags.append(i.strip('" '))
                        case _:
                            raise ValueError(f"Unknown tile/prop property '{prprty_name}'")
                
                if is_tiles:
                    self.tiles.append(currentTile)
                    print(currentTile) if DEBUG else None
                else:
                    self.props.append(currentTile)
    
    def encode(self, is_tiles: bool = True) -> str:
        return "none"

# Read the Init.txt file and parse it
def openInit(dirpath: str):
    with open(dirpath+"Init.txt") as f:
        init = f.read()
    
    #print(dirpath.split("\\"))

    #with open("\\".join(dirpath.split("\\")[:-2]) + "\\effectsInit.txt") as f:
        #effectsinit = f.read()
    
    #parser = EffectsInitParser(init, effectsinit)
    parser = GraphicsInitParser(init)
    parser.parse(True)
    return parser

if __name__ == '__main__':
    currDirectory = "F:\\GAME STUFF\\Drizzle\\Data\\Graphics\\"
    cool = openInit(currDirectory)

# TODO: MaterialsInitParser: make it parse nested ones, especially the texture and block properties.