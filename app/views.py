
import os
import cv2
import matplotlib.image as matimg
from app.face_recognition import faceRecognitionPipeLine

from flask import render_template,request

UPLOAD_FOLDER='static/upload'


def index():
  return render_template('index.html')


def app():
  return render_template('app.html')

def genderapp():
  if request.method=='POST':
    f=request.files['image_name']
    filename=f.filename
    #save aourimae
    path=os.path.join(UPLOAD_FOLDER,filename)
    f.save(path) 

    #get predict
    pred_image, prediction =faceRecognitionPipeLine(path)
    pred_filename='prediction_image.jpg'
    cv2.imwrite(f'./static/predict/{pred_filename}',pred_image)
    
  
    #generate report
    report=[]
    for i, obj in enumerate(prediction):
      gray_image=obj['roi']  #grayscale image(array)
      eigen_image=obj['eig_img'].reshape(100,100)
      gender_name=obj['prediction_name']
      score= round(obj['score']*100,2)

      #avinf in the folder

      gray_image_name= f'roi_{i}.jpg'
      eig_image_name= f'eigen_{i}.jpg'
      matimg.imsave(f'./static/predict/{gray_image_name}',gray_image,cmap='gray') 
      matimg.imsave(f'./static/predict/{eig_image_name}',eigen_image,cmap='gray') 

      #svae report
      report.append([gray_image_name,eig_image_name,gender_name, score])
      
    return render_template('gender.html',fileupload=True ,report=report) ##post request

  return render_template('gender.html',fileupload=False)  #get request
  

