import pandas as pd
import torch
from PIL import Image
import os
from torchvision import transforms
import cv2
from roboflow import Roboflow
from inference_sdk import InferenceHTTPClient
tone_model = torch.load("C:/Users/johns/Downloads/skin_tone_model2.pth")
hair_model = torch.load("C:/Users/johns/Downloads/hair_color_model.pth")
eye_model = torch.load("C:/Users/johns/Downloads/eye_color_model2.pth")
tone_classes = ['Dark', 'Fair', 'Medium']
hair_classes = ['Black', 'Blonde', 'Brunette', 'Red']
eye_classes = ['Blue', 'Brown', 'Green', 'Hazel']
transform = transforms.Compose([
    transforms.Resize((640,640)),
    transforms.ToTensor()
])
eye_transform = transforms.Compose([
    transforms.Resize((640,640)), transforms.ToTensor()])
def skin_care_scan():
        user_attributes = {}
        

        img = Image.open("input_img.jpg")
        tone_model.eval()
        with torch.inference_mode():
          img_trans = transform(img).unsqueeze(dim=0)
          output_tone = tone_model(img_trans)
          predicted_tone = torch.argmax(torch.softmax(output_tone, dim=1),dim=1)
          user_attributes['Skin_tone'] = (tone_classes[predicted_tone.item()])
          
        hair_model.eval()
        with torch.inference_mode():
          img_trans = transform(img).unsqueeze(dim=0)
          output_hair = hair_model(img_trans)
          predicted_hair = torch.argmax(torch.softmax(output_hair, dim=1),dim=1)
          user_attributes['Hair_color'] = (hair_classes[predicted_hair.item()])
        eye_model.eval()
        with torch.inference_mode():
          eye_trans = transform(img).unsqueeze(dim=0)
          output_eye = eye_model(eye_trans)
          predicted_eye = torch.argmax(torch.softmax(output_eye, dim=1),dim=1)
          user_attributes['Eye_color'] = (eye_classes[predicted_eye.item()])
        rf = Roboflow(api_key="YcRLabSlKRHADFLKgCvQ")
        project = rf.workspace("theaskin").project("skin-types")
        model = project.version(1).model
        prediction = model.predict('input_img.jpg')[0]
        user_attributes['Skin_type'] = (''.join(prediction['predicted_classes'])).capitalize()
        
        os.remove("input_img.jpg")
        return (user_attributes)

def begin_scan():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
        
            break
        
        cv2.imwrite("input_img.jpg", frame)
        return skin_care_scan()
    cam.release()
    cv2.destroyAllWindows()




df = pd.read_csv('https://github.com/ColinJ69/PocketDerm/raw/main/skin-care-products.csv', index_col=[0])


def recommend_products_by_user_features(skintone, skintype, eyecolor, haircolor, concerns):
    ddf = df[(df['Skin_Tone'] == skintone) & (df['Hair_Color'] == haircolor) & (df['Eye_Color'] == eyecolor) & (df['Skin_Type'] == skintype) & (df['Concerns'] == concerns)]
    recommendations = ddf[(ddf['Rating_Stars'].notnull())]
    data = recommendations[['Product', 'Rating_Stars', 'Brand', 'Product_Url', 'Category']]
    data.drop_duplicates(inplace=True, keep='last')
    data_good = data[data.Rating_Stars >= 4]
    data_final = data_good.sort_values('Rating_Stars', ascending=False).head()
    return(data_final)
recommendations = (recommend_products_by_user_features('Fair',
                                       'Dry','Hazel', 'Black', 'General'))


def disease_scan():
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="YcRLabSlKRHADFLKgCvQ"
    )

    result = CLIENT.infer('input_img.jpg', model_id="skin-disease-detection-s7zik/1")
    if len(result['predictions']) != 0:
        if result['predictions'][0]['confidence'] > 0.80:
            return(result['predictions'][0]['class'])
    os.remove('input_img.jpg')
    return 'We are not able to accurately predict that'

def begin_disease_scan():
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
        
            break
        
        cv2.imwrite("input_img.jpg", frame)
        return(disease_scan())
    cam.release()
    cv2.destroyAllWindows()
