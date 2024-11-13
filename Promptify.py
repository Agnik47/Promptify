import os
import google.generativeai as genai
import ipywidgets as widgets
from IPython.display import display, clear_output

#  API key
os.environ["GEMINI_API_KEY"] = "AIzaSyARFAE0dsEQm1rGVtaNGM6dnIZaUWuM9aY"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# prompt configuration
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

def generate_full_prompt(chat_session, user_input, prompt_type, word_count=None):
    try:
        custom_prompt = f"""
        You are an AI assistant that generates detailed yet concise prompts. The user will provide a brief input and specify a word count. Your response should:
        - Stay within {word_count} words, if specified.
        - Be complete, without cutting sentences awkwardly.
        - Follow a clear and logical structure.

        Prompt Type: {prompt_type}
        User's Input: {user_input}

        Please generate a complete prompt within {word_count or 'a reasonable'} word limit.
        """

        # Generate response using the chat session
        response = chat_session.send_message(custom_prompt)

        # If word count is specified, truncate the response ensuring sentences are complete
        if word_count:
            sentences = response.text.split('. ')
            final_text = ''
            current_word_count = 0

            for sentence in sentences:
                words_in_sentence = len(sentence.split())
                if current_word_count + words_in_sentence <= word_count:
                    final_text += sentence.strip() + '. '
                    current_word_count += words_in_sentence
                else:
                    break

            response_text = final_text.strip()
        else:
            response_text = response.text

        return response_text

    except Exception as e:
        return f"Error generating the prompt: {e}"



def handle_prompt_generation(user_input, prompt_type, word_count=None):
    #  (approx. 1.5 tokens per word)
    if word_count and word_count != 0:
        max_output_tokens = int(word_count * 1.5)
    else:
        max_output_tokens = 200  # Default value

    generation_config = get_generation_config(
        temperature=0.9,
        top_p=0.95,
        top_k=40,
        max_output_tokens=max_output_tokens
    )

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

# UI 
def generate_ui():
    # Prompt type options
    prompt_types = [
        "Zero-Shot", "One-Shot", "Few-Shot", "Question-Based", "Custom", 
        "Creative", "Instructional", "Descriptive", "Analysis", "Storytelling", "Summarization"
    ]

    print("Write Down small with instraction what is in your mind and what type of prompt you want?")    
    # Widgets for user input
    prompt_type_dropdown = widgets.Dropdown(
        options=prompt_types,
        description='Prompt Type:',
        disabled=False
    )

    user_input_box = widgets.Textarea(
        value='',
        placeholder='Enter your brief prompt here...',
        description='User Prompt:',
        disabled=False
    )

    word_count_box = widgets.IntText(
        value=None,
        placeholder='Enter word count (optional)',
        description='Word Count:',
        disabled=False
    )

    generate_button = widgets.Button(description="Generate Full Prompt")
    output_area = widgets.Output()

    # Button 
    def on_button_click(b):
        with output_area:
            clear_output()
            user_input = user_input_box.value
            prompt_type = prompt_type_dropdown.value
            word_count = word_count_box.value

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Goodbye! See you next time.")
                return

            generated_prompt = handle_prompt_generation(user_input, prompt_type, word_count)
            print(f"\nGenerated Full Prompt: \n{generated_prompt}\n")

    generate_button.on_click(on_button_click)

    # Display widgets
    display(user_input_box, prompt_type_dropdown, word_count_box, generate_button, output_area)

# Call 
generate_ui()
