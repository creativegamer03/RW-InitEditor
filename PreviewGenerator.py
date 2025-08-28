# Based on the preview generator for Rained
# TODO: Palette application for palette previews

from PIL import Image
import io
import Tiles as tiles

def generate_palette(category_color: tuple):
    palette_dict = {}
    for sublayer in range(30):
        lf = sublayer / 30
        a = lf
        palette_dict[30-(sublayer+1)] = {
            "up": (
                int(category_color[0] * (1.0 - a) + (category_color[0] * 0.8) * a),
                int(category_color[1] * (1.0 - a) + (category_color[1] * 0.8) * a),
                int(category_color[2] * (1.0 - a) + (category_color[2] * 0.8) * a)
            ),
            "middle": (
                int(category_color[0] * (1.0 - a) + (category_color[0] * 0.5) * a),
                int(category_color[1] * (1.0 - a) + (category_color[1] * 0.5) * a),
                int(category_color[2] * (1.0 - a) + (category_color[2] * 0.5) * a)
            ),
            "down": (
                int(category_color[0] * (1.0 - a) + (category_color[0] * 0.2) * a),
                int(category_color[1] * (1.0 - a) + (category_color[1] * 0.2) * a),
                int(category_color[2] * (1.0 - a) + (category_color[2] * 0.2) * a)
            )
        }
    return palette_dict

def fetch_palette(palette_id: str):
    raise NotImplementedError

class PreviewGenerator:
    def __init__(self, palette: dict|str = "color", **kwgs):
        if palette == "color":
            self.palette = None
        else:
            if isinstance(palette, dict):
                self.palette = palette
            else:
                self.palette = fetch_palette(palette)
    
    def __crop__(self):
        raise NotImplementedError

    def generatePreview(self):
        raise NotImplementedError

class TilePreviewGenerator(PreviewGenerator):
    def __init__(self, tiles: list[tiles.Tile], **kwgs):
        super().__init__(**kwgs)
        self.tiles = tiles
    
    def __crop__(self, tile: tiles.Tile, tile_image: Image.Image, tile_frame_size: tuple[int, int], variation: int = 1):
        total_sublayers = 20 if tile.specs2 != None else 10
        temp_repeatLayers = tile.repeatLayers
        temp_repeatLayers.reverse() if isinstance(temp_repeatLayers, list) else None

        if tile.type_ == tiles.TileTypes.RockType or tile.type_ == tiles.TileTypes.SandType:
            box = ((tile_frame_size[0] * abs(variation - 1)), 0, (tile_frame_size[0] * variation), tile_frame_size[1])

            for sublayer in range(total_sublayers):
                cropped = tile_image.crop(box)
                cropped = cropped.convert("RGBA")
                cropped_data = cropped.getdata()
                new_data = []

                for data in cropped_data:
                    if data[0] == 255 and data[1] == 255 and data[2] == 255: # WHITE
                        new_data.append((255, 255, 255, 0))
                    elif data[0] == 0 and data[1] == 0 and data[2] == 255: # BLUE (UP)
                        new_data.append(self.palette[sublayer]["up"] + (255,))
                    elif data[0] == 0 and data[1] == 255 and data[2] == 0: # GREEN (MIDDLE)
                        new_data.append(self.palette[sublayer]["middle"] + (255,))
                    elif data[0] == 255 and data[1] == 0 and data[2] == 0: # RED (DOWN)
                        new_data.append(self.palette[sublayer]["down"] + (255,))
                    else:
                        new_data.append(data)
                
                cropped.putdata(new_data)
                yield cropped
        
        elif tile.type_ == tiles.TileTypes.Box:
            box = ((tile_frame_size[0] * abs(variation - 1)), 0, (tile_frame_size[0] * variation), tile_frame_size[1])

        else:
            for frame in range(len(temp_repeatLayers) if temp_repeatLayers != None else 1):
                box = ((tile_frame_size[0] * abs(variation - 1)),
                    ((len(temp_repeatLayers) if temp_repeatLayers != None else 1) - (frame + 1)) * tile_frame_size[1],
                    (tile_frame_size[0] * variation),
                    ((len(temp_repeatLayers) if temp_repeatLayers != None else 1) - frame) * tile_frame_size[1]
                )

                for _ in range(temp_repeatLayers[frame] if temp_repeatLayers != None else total_sublayers):
                    cropped = tile_image.crop(box)
                    cropped = cropped.convert("RGBA")
                    cropped_data = cropped.getdata()
                    new_data = []

                    for data in cropped_data:
                        if data[0] == 255 and data[1] == 255 and data[2] == 255: # WHITE
                            new_data.append((255, 255, 255, 0))
                        elif data[0] == 0 and data[1] == 0 and data[2] == 255: # BLUE (UP)
                            new_data.append(self.palette[frame]["up"] + (255,))
                        elif data[0] == 0 and data[1] == 255 and data[2] == 0: # GREEN (MIDDLE)
                            new_data.append(self.palette[frame]["middle"] + (255,))
                        elif data[0] == 255 and data[1] == 0 and data[2] == 0: # RED (DOWN)
                            new_data.append(self.palette[frame]["down"] + (255,))
                        else:
                            new_data.append(data)
                    
                    cropped.putdata(new_data)
                    yield cropped

    def generatePreview(self, tile_name: str, category: str, variation: int = 1, graphicsDirectory: str = None, show_editor_preview: bool = False):
        theTile = None
        for tile in self.tiles:
            if tile.name == tile_name and tile.category.name == category:
                theTile = tile
                break
        
        if theTile == None:
            raise ValueError(f"Tile named \"{tile_name}\" not found in loaded tile init file.")

        tileImage = Image.open((graphicsDirectory if graphicsDirectory else "") + theTile.name + ".png")

        if show_editor_preview:
            tileFrameW = 16 * theTile.size[0]
            tileFrameH = 16 * theTile.size[1]

            previewImage = Image.new("RGBA", (tileFrameW, tileFrameH))

            cropped = tileImage.crop((
                0,
                (tileImage.size[1] - tileFrameH),
                tileFrameW,
                (tileImage.size[1])
            )).convert("RGBA")
            data = []
            
            for crd in cropped.getdata():
                if crd[0] == 255 and crd[1] == 255 and crd[2] == 255:
                    data.append((255, 255, 255, 0))
                else:
                    data.append(crd)
            
            previewImage.putdata(data)

        else:
            self.palette = generate_palette(theTile.category.color)

            tileFrameW = 20 * (theTile.size[0] + (theTile.bufferTiles * 2))
            tileFrameH = 20 * (theTile.size[1] + (theTile.bufferTiles * 2))

            previewImage = Image.new("RGBA", (tileFrameW, tileFrameH))

            for sublayer in self.__crop__(theTile, tileImage, (tileFrameW, tileFrameH), variation):
                previewImage.paste(sublayer, (0, 0), sublayer)
        
        return previewImage