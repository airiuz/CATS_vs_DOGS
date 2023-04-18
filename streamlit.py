import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
import cv2
st.set_page_config(page_title='Cats vs Dogs klassifikatsiya',layout='wide')
model = tf.keras.models.load_model("Model")

title = "Cats vs Dogs dataseti yordamida o'qitilgan modelni sinovdan o'tkazish"
header1 = "Model haqida ma'lumot"
header2 = "Faylni yuklang va predict qiling"

data_main = [["optimizer","Adam"],["loss funksiyasi","Categorical Cross Entropy"],
              ["epochs","5"],["train loss qiymati","0.4166"],
             ["train accuracy qiymati","0.8105"],
             ["evaluate loss qiymati","0.5621"],
             ["evaluate accuracy qiymati","0.746"],
             ["parametrlar soni","17 009 088"]]

information = pd.DataFrame(data_main,columns=["Parametrlar","Qiymatlar"])

st.markdown("<h1 style='text-align: center;font-size: 30px;'>"+title+"</h1>", unsafe_allow_html=True)
col1,col2 = st.columns(2)
col1.markdown("<h1 style='text-align: center;font-size: 20px;'>"+header1+"</h1>", unsafe_allow_html=True)
col1.dataframe(information,use_container_width=True)

col2.markdown("<h1 style='text-align: center;font-size: 20px;'>"+header2+"</h1>", unsafe_allow_html=True)
image = col2.file_uploader("Faylni yuklang")

if image is not None:

    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    c1,c2,c3 = col2.columns(3)
    c2.image(img, channels="BGR",use_column_width=True)
    
    if c2.button("Predict",use_container_width=True):
        # normalizatsiya
        image = np.array(img)
        image = np.array(cv2.resize(image,(256,256),interpolation = cv2.INTER_AREA))
        image = np.array(image).astype('float32')/255.0
        image = image.reshape(1,256,256,3)
        
        classlar = ["Cat","Dog"]
        one_hot = model.predict(image)
        index = np.argmax(one_hot)
        predict = classlar[index]
        probability=one_hot[0][index]
        
        result = {"Atributlar":["Class nomi","Ehtimollik"],"Qiymatlar":[predict,probability]}
        
        col1.dataframe(result,use_container_width=True)
