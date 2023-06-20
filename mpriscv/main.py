import ctypes
import numpy as np
import cv2
from flask import Flask, Response

# Load the shared library containing the mpriscv function
my_lib = ctypes.CDLL("./mpriscv/mpriscv.so")

# Define the argument types
my_lib.mpriscv.argtypes = [
    ctypes.c_int,              # sel_img
    ctypes.POINTER(ctypes.c_float),  # t0
    ctypes.POINTER(ctypes.c_float),  # t1
    ctypes.POINTER(ctypes.c_float),  # t2
    ctypes.POINTER(ctypes.c_float),  # t3
    ctypes.POINTER(ctypes.c_float),  # t4
    ctypes.POINTER(ctypes.c_float)   # t5
]

# Define the return type
my_lib.mpriscv.restype = ctypes.POINTER(ctypes.c_uint8)

# Call the mpriscv function
sel_img = 2
t0 = ctypes.c_float(0.0)
t1 = ctypes.c_float(0.0)
t2 = ctypes.c_float(0.0)
t3 = ctypes.c_float(0.0)
t4 = ctypes.c_float(0.0)
t5 = ctypes.c_float(0.0)
result = my_lib.mpriscv(sel_img, ctypes.byref(t0), ctypes.byref(t1), ctypes.byref(t2), ctypes.byref(t3), ctypes.byref(t4), ctypes.byref(t5))

# Access the returned array
# Convert the result to a numpy array
array_size = 240 * 240  # Adjust the array size according to your specific requirements
array = ctypes.cast(result, ctypes.POINTER(ctypes.c_uint8 * array_size)).contents
image_data = np.array(array, dtype=np.uint8)

# Reshape the 1D array to a 2D image array
image = np.reshape(image_data, (240, 240))

# Create a Flask app
app = Flask(__name__)

# Route for displaying the image
@app.route("/")
def display_image():
    # Encode the image as JPEG
    _, jpeg_image = cv2.imencode(".jpg", image)

    # Create a Flask response with the encoded image
    response = Response(jpeg_image.tobytes(), mimetype="image/jpeg")

    return response

# Run the Flask app
if __name__ == "__main__":
    app.run()