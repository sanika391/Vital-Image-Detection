import streamlit as st
from pathlib import Path
import google.generativeai as genai

st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")
st.image(r"image.png", width=150)
# Configure your API key
try:
    from api_keys import api_key
    genai.configure(api_key=api_key)
except ImportError:
    st.error("API key file not found. Please ensure you have 'api_key.py' with a valid 'api_key' variable.")
    st.stop()
except Exception as e:
    st.error(f"Error configuring API key: {e}")
    st.stop()

# Generation configuration
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 632,
    "max_output_tokens": 4096,
}  

# Safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
       "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE" 
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the image.

Your responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or intervention.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues. 
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."

Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.
"""

try:
    model = genai.GenerativeModel(
        model_name="gemini-pro-vision",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"Error initializing GenerativeModel: {e}")
    st.stop()


uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])
submit_button = st.button("Generate the Analysis")

if submit_button:
    if uploaded_file is not None:
        try:
            image_data = uploaded_file.getvalue()
            
            # Making our image ready
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": image_data
                },
            ]
            
            # Making our prompt ready
            prompt_parts = [
                image_parts[0],
                system_prompt,
            ]
            
            # Generate response based on prompt and image
            try:
                response = model.generate_content(prompt_parts)
                st.write(response.text)
            except genai.ApiException as e:
                st.error(f"API error: {e.status_code} - {e.message}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
        except Exception as e:
            st.error(f"Error processing the uploaded file: {e}")
    else:
        st.error("Please upload a file before submitting.")