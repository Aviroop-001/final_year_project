from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home_route():
    return "home sweet home", 200

@app.route('/upscale', methods=['POST'])
def upscale_image():
    try:
        # Get the image from the request
        file = request.files['image']

        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Convert to grayscale if needed
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply histogram equalization
        enhanced_image = cv2.equalizeHist(gray)

        # Convert back to color if needed
        enhanced_image = cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2BGR)

        # Save the enhanced image
        enhanced_image_path = "enhanced_image.png"
        cv2.imwrite(enhanced_image_path, enhanced_image)

        return jsonify({"message": "Image upscaled successfully", "upscaled_image_path": enhanced_image_path})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(threaded=True)
