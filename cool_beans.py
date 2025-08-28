from flask import Flask, render_template, jsonify, request, send_file
from InitEditor import GraphicsInitParser, openInit
from PreviewGenerator import TilePreviewGenerator
from io import BytesIO

app = Flask(__name__)
app.json.sort_keys = False
currDirectory = "C:\\Users\\CreativeGamer03\\Desktop\\files\\dev_stuff\\RWE+\\drizzle\\Data\\Graphics\\"

def serve_pil_image(pil_image):
    img_io = BytesIO()
    pil_image.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")

@app.route("/")
def index():
    return render_template("index.html")
    #return "Hi"

@app.route("/cool")
def cool():
    cool = openInit(currDirectory)
    return jsonify([t.serialize() for t in cool.tiles])

@app.route("/preview/<string:category>/<string:tilename>", methods = ["GET"])
def fetch_preview(category: str, tilename: str):
    variation = request.args["v"] if "v" in request.args.keys() else "1"
    show_editor_preview = request.args["sep"] if "sep" in request.args.keys() else "0"
    cool = openInit(currDirectory)
    
    previewGenerator = TilePreviewGenerator(cool.tiles)
    image = previewGenerator.generatePreview(tilename, category, int(variation), currDirectory, True if show_editor_preview == "1" else False)
    image_response = serve_pil_image(image)
    image_response.headers["Cache-Control"] = "public, max-age=31536000"

    return image_response

app.run(host="0.0.0.0", port="10", debug=True)