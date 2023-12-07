from flask import Flask, request, jsonify
import requests
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionUpscalePipeline
from diffusers import StableDiffusionXLImg2ImgPipeline
from diffusers.utils import load_image
import torch

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home_route():
    return "home sweet home", 200

# Load model and move it to GPU
model_id = "stabilityai/stable-diffusion-xl-refiner-1.0"
pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16", use_safetensors=True)

@app.route('/upscale', methods=['POST'])
def upscale_image():
    try:
        # Get the image from the request
        file = request.files['image']
        
        url = "https://huggingface.co/datasets/patrickvonplaten/images/resolve/main/aa_xl/000000009.png"

        init_image = load_image(url).convert("RGB")
        prompt = "a photo of an astronaut riding a horse on mars"
        image = pipe(prompt, image=init_image).images
        upscaled_image_path = "upscaled_image.png"
        image.save(upscaled_image_path)

        return jsonify({"message": "Image upscaled successfully", "upscaled_image_path": upscaled_image_path})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
