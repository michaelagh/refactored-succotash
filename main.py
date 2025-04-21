from flask import Flask, render_template, jsonify, request
from ves import generate_image_from_ves_code, blur_image, invert_colors, greyscale, simulate_protanopia
import io
import base64

app = Flask(__name__, template_folder=".")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render():
    data = request.get_json()

    ves_code = data.get('ves', '') 
    filter_name = data.get('filter', 'ORIGINAL')  

    ves_code_lines = ves_code.splitlines()
    obr = generate_image_from_ves_code(ves_code_lines)

    if filter_name == 'BLUR':
        obr = blur_image(obr)
    elif filter_name == 'INVERTED':
        obr = invert_colors(obr)
    elif filter_name == 'GREYSCALE':
        obr = greyscale(obr)
    elif filter_name == 'COLORBLIND':
        obr = simulate_protanopia(obr)

    img_io = io.BytesIO()
    obr.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return jsonify({"image": img_base64}) 

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
