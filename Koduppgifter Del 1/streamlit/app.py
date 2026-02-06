import streamlit as st
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image

@st.cache_resource
def load_model():
    return ResNet50(weights="imagenet")

model = load_model()

st.write("Ladda upp en bild här")

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    
    # Convert to RGB if image has alpha channel (RGBA) or is grayscale
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    st.image(img, caption="Uppladdad bild", use_container_width=True)
    
    img_resized = img.resize((224, 224))
    x = image.img_to_array(img_resized)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    with st.spinner("Analyserar bild.."):
        preds = model.predict(x)
        results = decode_predictions(preds, top=3)[0]
    
    st.subheader("Resultat:")
    for i, (imagenet_id, label, score) in enumerate(results):
        st.write(f"{i+1}. **{label}** - {score*100:.2f}%")