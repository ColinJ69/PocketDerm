from pathlib import Path
import torch
import requests
from PIL import Image
import os
from torchvision import transforms
import cv2
import requests
from roboflow import Roboflow
model = torch.load('skin_tone_model.pth')
class_names = ['Dark', 'Fair', 'Tan']
transform = transforms.Compose([
    transforms.Resize((320,320)),
    transforms.ToTensor()
])
rf = Roboflow(api_key="YcRLabSlKRHADFLKgCvQ")
project_acne = rf.workspace("signlanguagetospeech").project("acne-severity-hyuk1")
acne_sev_model = project_acne.version(2).model
project_stype = rf.workspace("theaskin").project("skin-types")
skin_type_model = project_stype.version(1).model

def test(frame):
        attrs = []
        img_path = cv2.imread("input_img.zip")
        cv2.imwrite("input_img.jpg", frame)
        
        img = Image.open("input_img.jpg")
        model.eval()
        with torch.inference_mode():
          img_trans = transform(img).unsqueeze(dim=0)
          output = model(img_trans)
        
        predicted_class = torch.argmax(torch.softmax(output, dim=1),dim=1)
        attrs.append(class_names[predicted_class.item()])
        prediction_acne = (acne_sev_model.predict('input_img.jpg'))[0]
        prediction_stype = (skin_type_model.predict('input_img.jpg'))[0]
        attrs.append(''.join(prediction_acne['predicted_classes']))
        attrs.append(''.join(prediction_stype['predicted_classes']))
        os.remove("input_img.jpg")
        return attrs
def start():
  cam = cv2.VideoCapture(0)
  while True:
      ret, frame = cam.read()
      if not ret:
          break
      cv2.imshow('frame',frame)
      print(test(frame))
      cam.release()
      cv2.destroyAllWindows()
start()
