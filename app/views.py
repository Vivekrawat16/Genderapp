import os
import cv2
import matplotlib.image as matimg
from app.face_recognition import faceRecognitionPipeLine

from flask import render_template, request

UPLOAD_FOLDER = 'static/upload'

def index():
    return render_template('index.html')

def app():
    return render_template('app.html')

def genderapp():
    if request.method == 'POST':
        f = request.files['image_name']
        filename = f.filename

        # Save image
        path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(path)

        # Predict
        pred_image, prediction = faceRecognitionPipeLine(path)
        pred_filename = 'prediction_image.jpg'
        cv2.imwrite(f'./static/predict/{pred_filename}', pred_image)

        # Generate report
        report = []
        for i, obj in enumerate(prediction):
            gray_image = obj['roi']
            eigen_image = obj['eig_img'].reshape(100, 100)
            gender_name = obj['prediction_name']
            score = round(obj['score'] * 100, 2)

            # Save grayscale and eigenface images
            gray_image_name = f'roi_{i}.jpg'
            eig_image_name = f'eigen_{i}.jpg'
            matimg.imsave(f'./static/predict/{gray_image_name}', gray_image, cmap='gray')
            matimg.imsave(f'./static/predict/{eig_image_name}', eigen_image, cmap='gray')

            report.append([gray_image_name, eig_image_name, gender_name, score])

        return render_template('gender.html', fileupload=True, report=report)

    # GET request fallback
    return render_template('gender.html', fileupload=False)
