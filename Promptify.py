import os
import google.generativeai as genai
import ipywidgets as widgets
from IPython.display import display, clear_output

# Set your API key
os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"  # Replace with your API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define prompt configuration
def get_generation_config(temperature=0.8, top_p=0.95, top_k=40, max_output_tokens=150):
    return {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_output_tokens,
        "response_mime_type": "text/plain",
    }

# Initialize model
def initialize_model(model_name="gemini-1.5-flash", generation_config=None):
    if generation_config is None:
        generation_config = get_generation_config()

    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
        )
        return model
    except Exception as e:
        print(f"Error initializing the model: {e}")
        return None

# Start chat session
def start_chat_session(model):
    try:
        chat_session = model.start_chat(history=[])
        return chat_session
    except Exception as e:
        print(f"Error starting chat session: {e}")
        return None

# Function to handle explicit content and generate a prompt
def handle_explicit_content(user_input):
    # List of explicit keywords
    explicit_keywords = ["naked", "sex", "porn", "explicit", "adult", "vulgar"]

    if any(keyword in user_input.lower() for keyword in explicit_keywords):
        # Custom message for explicit content
        return """
        
        
        
        """
    else:
        return None  # No explicit content found

# Function to generate full prompt
def generate_full_prompt(chat_session, user_input, prompt_type):
    try:
        # Check for explicit content before generating the prompt
        explicit_message = handle_explicit_content(user_input)
        if explicit_message:
            return explicit_message

        custom_prompt = f"""
        You are an AI assistant that helps users generate detailed prompts based on their brief input. The user will provide a short prompt and select the type of prompt (e.g., few-shot, one-shot, question-based). Your task is to generate a structured, well-defined prompt tailored to the selected type. 

        Prompt Type: {prompt_type}
        User's Input: {user_input}

        Your generated prompt should be:
        1. Clear and actionable
        2. Structured with detailed instructions
        3. Contextualized for the selected prompt type
        """
        
        # Send message to the AI model to generate the prompt
        response = chat_session.send_message(custom_prompt)
        return response.text

    except Exception as e:
        return f"Error generating the prompt: {e}"

# Function to handle prompt generation
def handle_prompt_generation(user_input, prompt_type):
    generation_config = get_generation_config(temperature=0.9, top_p=0.95, top_k=40, max_output_tokens=200)
    model = initialize_model(model_name="gemini-1.5-flash", generation_config=generation_config)

    if not model:
        print("Error initializing the model. Exiting...")
        return

    try:
        chat_session = start_chat_session(model)
        if not chat_session:
            print("Error starting chat session. Exiting...")
            return

        generated_prompt = generate_full_prompt(chat_session, user_input, prompt_type)
        return generated_prompt

    except Exception as e:
        print(f"An error occurred: {e}")
        return

# UI Components using ipywidgets
def generate_ui():
    # Prompt type options
    prompt_types = [
        "Zero-Shot", "One-Shot", "Few-Shot", "Question-Based", "Custom", 
        "Creative", "Instructional", "Descriptive", "Analysis"
    ]
    
    prompt_type_dropdown = widgets.Dropdown(
        options=prompt_types,
        description='Prompt Type:',
        disabled=False
    )

    # Textbox for user input
    user_input_box = widgets.Textarea(
        value='',
        placeholder='Enter your brief prompt here...',
        description='User Prompt:',
        disabled=False
    )

    # Button to generate the prompt
    generate_button = widgets.Button(description="Generate Full Prompt")

    # Output area to display results
    output_area = widgets.Output()

    # Define button click action
    def on_button_click(b):
        with output_area:
            clear_output()
            user_input = user_input_box.value
            prompt_type = prompt_type_dropdown.value

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Goodbye! See you next time.")
                return

            generated_prompt = handle_prompt_generation(user_input, prompt_type)
            print(f"\nGenerated Full Prompt: \n{generated_prompt}\n")

    generate_button.on_click(on_button_click)

    # Display the widgets
    display(user_input_box, prompt_type_dropdown, generate_button, output_area)

# Call the UI function to start
generate_ui()
