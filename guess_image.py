import streamlit as st
import base64
import ollama
from PIL import Image
import io

def init_session_state():
    """Initialize session state variables"""
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_challenge' not in st.session_state:
        st.session_state.current_challenge = None
    if 'challenges' not in st.session_state:
        st.session_state.challenges = [
            "Find an image containing something red",
            "Show me a landscape photo",
            "Find an image with text in it",
            "Show me a picture of food",
            "Find an image with multiple objects",
        ]

def image_to_base64(img):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    img.save(buffered, format='PNG')
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def check_success(response, challenge):
    """Improved success checking logic"""
    response_lower = response.lower()
    challenge_lower = challenge.lower()
    
    # Define success criteria based on challenge type
    if "red" in challenge_lower:
        # Check if response indicates presence of red and doesn't deny it
        return ("red" in response_lower and 
                "no red" not in response_lower and 
                "not red" not in response_lower and 
                "isn't red" not in response_lower)
    
    elif "landscape" in challenge_lower:
        return ("landscape" in response_lower and 
                "not a landscape" not in response_lower)
    
    elif "text" in challenge_lower:
        return ("text" in response_lower and 
                "no text" not in response_lower and 
                "without text" not in response_lower)
    
    elif "food" in challenge_lower:
        return ("food" in response_lower and 
                "no food" not in response_lower and 
                "not food" not in response_lower)
    
    elif "multiple objects" in challenge_lower:
        indicators = ["multiple", "several", "many", "different", "various"]
        return any(indicator in response_lower for indicator in indicators)
    
    return False

def get_vision_response(base64_image, challenge):
    """Get response from Ollama vision model with improved prompt"""
    try:
        response = ollama.chat(
            model='llama3.2-vision:latest',
            messages=[{
                'role': 'user',
                'content': (
                    f"Analyze this image specifically for the following challenge: {challenge}. "
                    "First, describe what you see. Then, explicitly state whether the image "
                    "meets the challenge criteria or not, and why."
                ),
                'images': [base64_image]
            }]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def new_challenge():
    """Get the next challenge"""
    if st.session_state.challenges:
        st.session_state.current_challenge = st.session_state.challenges.pop(0)
    else:
        st.session_state.current_challenge = "Game Over!"

def reset_game():
    """Reset the game state"""
    st.session_state.score = 0
    st.session_state.current_challenge = None
    st.session_state.challenges = [
        "Find an image containing something red",
        "Show me a landscape photo",
        "Find an image with text in it",
        "Show me a picture of food",
        "Find an image with multiple objects",
    ]

def main():
    st.set_page_config(page_title="Vision Guessing Game", layout="wide")
    
    # Initialize session state
    init_session_state()
    
    # Title and score
    st.title("Vision Guessing Game")
    st.subheader(f"Current Score: {st.session_state.score}")
    
    # Game controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("New Challenge"):
            new_challenge()
            
        if st.button("Reset Game"):
            reset_game()
    
    # Display current challenge
    if st.session_state.current_challenge:
        st.info(f"Current Challenge: {st.session_state.current_challenge}")
    else:
        st.warning("Click 'New Challenge' to start!")
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=['png', 'jpg', 'jpeg'],
        key='uploader'
    )
    
    # Process uploaded image
    if uploaded_file and st.session_state.current_challenge != "Game Over!":
        # Display image
        image = Image.open(uploaded_file)
        image.thumbnail((400, 400))
        st.image(image, caption="Uploaded Image")
        
        # Get model response
        with st.spinner("Getting vision model response..."):
            base64_img = image_to_base64(image)
            response = get_vision_response(base64_img, st.session_state.current_challenge)
            
            # Display response
            st.text_area("Model Response:", value=response, height=150)
            
            # Check for success with improved logic
            if check_success(response, st.session_state.current_challenge):
                st.session_state.score += 10
                st.balloons()
                st.success("Challenge completed! +10 points")
            else:
                st.error("Try again! The image doesn't seem to match the challenge.")

if __name__ == "__main__":
    main()