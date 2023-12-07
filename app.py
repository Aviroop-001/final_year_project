from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home_route():
    return "home sweet home", 200

@app.route('/upscale', methods=['POST'])
def upscale_image():
    try:
        file = request.files['image']

        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        enhanced_image = cv2.equalizeHist(gray)
        enhanced_image = cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2BGR)

        # Save the enhanced image
        # enhanced_image_path = "enhanced_image.png"
        # cv2.imwrite(enhanced_image_path, enhanced_image)
        # return jsonify({"message": "Image upscaled successfully", "upscaled_image_path": enhanced_image_path})

        image_io = BytesIO()
        cv2.imwrite(image_io, enhanced_image)
        image_io.seek(0)

        # Return the image in the response
        return send_file(image_io, mimetype='image/png', as_attachment=True, download_name='enhanced_image.png')

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
