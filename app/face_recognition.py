import numpy as np
import pandas as pd
import sklearn 
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import cv2

haar = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
model_svm = pickle.load(open('./model/model_svm.pickle', mode='rb'))
pca_models = pickle.load(open('./model/pca_dict.pickle', mode='rb'))

model_pca = pca_models['pca']   # PCA model
mean_face_arr = pca_models['mean_face']
svc = SVC(probability=True) 

def faceRecognitionPipeLine(filename):
    # Step-01: Read image
    img = cv2.imread(filename)
    
    # Step-02: Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Step-03: Detect faces using Haar Cascade
    faces = haar.detectMultiScale(gray, 1.5, 3)
    
    predictions = []
    for x, y, w, h in faces:
        roi = gray[y:y+h, x:x+w]
        
        # Step-04: Normalize (0-1)
        roi = roi / 255.0
        
        # Step-05: Resize to (100, 100)
        if roi.shape[1] > 100:
            roi_resize = cv2.resize(roi, (100, 100), cv2.INTER_AREA)
        else:
            roi_resize = cv2.resize(roi, (100, 100), cv2.INTER_CUBIC)
        
        # Step-06: Flatten (1x10000)
        roi_reshape = roi_resize.reshape(1, 10000)
        
        # Step-07: Subtract mean face
        roi_mean = roi_reshape - mean_face_arr
        
        # Step-08: Apply PCA
        eigen_image = model_pca.transform(roi_mean)
        
        # Step-09: Get inverse PCA for visualization
        eig_img = model_pca.inverse_transform(eigen_image)
        
        # Step-10: Predict gender using SVM
        results = model_svm.predict(eigen_image)
        prob_score = model_svm.predict_proba(eigen_image)
        prob_score_max = prob_score.max()
        
        # Fix: Invert prediction if needed
        predicted_gender = 'female' if results[0] == 'male' else 'male'
        
        # Step-11: Draw bounding box and label
        text = f"{predicted_gender} : {prob_score_max*100:.0f}%"
        color = (255, 255, 0) if predicted_gender == 'male' else (255, 0, 255)  # Yellow for male, pink for female
        
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        cv2.rectangle(img, (x, y-40), (x+w, y), color, -1)
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
        
        predictions.append({
            'roi': roi,
            'eig_img': eig_img,
            'prediction_name': predicted_gender,
            'score': prob_score_max
        })
    
    return img, predictions  # <-- Correct indentation (aligned with 'def')