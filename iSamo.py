from flask import Flask, request, render_template, send_file
import rawpy
import io
import PIL.Image

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/apply_filter', methods=['POST'])
def apply_filter():
  # Get the file from the request
  file = request.files['file']

  # Open the DNG file
  with rawpy.imread(file) as raw:
    # Extract the metadata
    metadata = raw.metadata
    # Apply the filter using the metadata
    raw.apply_color_matrix(metadata.color_matrix1)

    # Convert the image data to a PIL Image
    image = PIL.Image.frombytes(raw.color_space, raw.sizes, raw.raw_image_visible)

  # Save the image to a memory buffer
  buffer = io.BytesIO()
  image.save(buffer, 'JPEG')
  buffer.seek(0)

  # Return the image as a response
  return send_file(buffer, mimetype='image/jpeg')
