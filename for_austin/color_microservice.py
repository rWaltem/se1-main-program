import flask
import random

app = flask.Flask(__name__)

PRESET_COLORS = {
    "red": "#ff0000",
    "green": "#00ff00",
    "blue": "#0000ff",
    "pink": "#FFB7C5"
}

def apply_transparency(color, value):
    # value should be a percent from 0 - 100
    hex_val = round((value / 100) * 255)
    alpha = format(hex_val, '02x')

    return f"{color}{alpha}".lower()

@app.route("/color", methods=["POST"])
def color_picker():
    data = flask.request.get_json()

    request_color = data.get("color")
    transparency = data.get("transparency")  # optional, expected as percent value

    if not isinstance(request_color, str):
        return flask.jsonify({"error": "'color' field must be a string"})

    request_color = request_color.lower()

    # random preset
    if request_color == "random_preset":
        color_name, hex_color = random.choice(list(PRESET_COLORS.items()))

    # random hex color
    elif request_color == "random":
        color_name = "random"
        hex_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    # preset color
    elif request_color in PRESET_COLORS:
        color_name = request_color
        hex_color = PRESET_COLORS[color_name]

    else:
        return flask.jsonify({"error": f"'{request_color}' is not a valid preset"})


    # apply transparnecy
    if transparency is not None:
        hex_color = apply_transparency(hex_color, transparency)

    return flask.jsonify({
        "color_name": color_name,
        "hex": hex_color
    })

if __name__ == "__main__":
    app.run(debug=True)
