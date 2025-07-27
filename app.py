# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from PIL import Image
# import io

# app = FastAPI()

# @app.post("/upload-image/")
# async def upload_image(file: UploadFile = File(...)):
#     try:
#         # Read image file
#         image = Image.open(io.BytesIO(await file.read()))

#         # Convert to RGB (in case it's grayscale or has transparency)
#         image = image.convert("RGB")

#         # Save the image (optional, for debugging)
#         image.save("uploaded_image.jpg")

#         return JSONResponse(content={"filename": file.filename, "message": "Image uploaded successfully!"})

#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=400)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io
from PIL import Image


# Load the trained model
model = load_model("C:/Users/vishn/Downloads/cnn_model.h5")

# Class labels
class_labels = ["Mild Demented", "Moderate Demented", "Non Demented", "Very Mild Demented"]

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains (change to specific domain in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


# Function to preprocess the image
def preprocess_image(img):
    img = img.resize((128, 128))  # Resize to match model input
    img = np.array(img) / 255.0   # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# API endpoint to upload and predict image
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Read and open image
        img = Image.open(io.BytesIO(await file.read()))
        img = img.convert("RGB")  # Ensure RGB format

        # Preprocess image
        img = preprocess_image(img)

        # Perform model prediction
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = float(np.max(predictions))

        return JSONResponse(content={
            "filename": file.filename,
            "prediction": class_labels[predicted_class],
            "confidence": confidence
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

