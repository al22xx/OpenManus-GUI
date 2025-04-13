import gradio as gr
import os
import httpx
import anthropic
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
from file_processor import process_file

load_dotenv()

def get_active_model():
    return os.getenv("ACTIVE_MODEL", "openai")

def get_api_key(model_name):
    return os.getenv(f"{model_name.upper()}_API_KEY", "")

def save_settings_to_env(model_name, api_key):
    env_path = "/workspace/.env"
    current_settings = {}
    
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    current_settings[key] = value

    current_settings["ACTIVE_MODEL"] = model_name
    current_settings[f"{model_name.upper()}_API_KEY"] = api_key

    with open(env_path, "w") as f:
        for key, value in current_settings.items():
            f.write(f"{key}={value}\n")

    os.environ.update(current_settings)
    return f"✅ Saved {model_name} settings!"

def update_key_input(model_name):
    return gr.update(value=get_api_key(model_name))

def handle_uploaded_files(files):
    combined = []
    for file in files:
        try:
            content = process_file(file.name)
            combined.append(f"📁 {os.path.basename(file.name)}:\n{content}")
        except Exception as e:
            combined.append(f"❌ Error processing {file.name}: {str(e)}")
    return "\n\n".join(combined)

def generate_response(query, files):
    active_model = get_active_model()
    api_key = get_api_key(active_model)
    file_content = handle_uploaded_files(files) if files else ""
    full_query = f"{query}\n\n{file_content}" if file_content else query

    try:
        if active_model == "claude":
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                messages=[{"role": "user", "content": full_query}]
            )
            return response.content[0].text

        elif active_model == "gemini":
            try:
                genai.configure(
                    api_key=os.getenv("GEMINI_API_KEY"),
                    transport='rest',
                    client_options={
                        "api_endpoint": "generativelanguage.googleapis.com"
                    }
                )
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                # Simplified proper format
                response = model.generate_content(
                    full_query,  # Directly pass the text input
                    generation_config={
                        "temperature": 0.5,
                        "max_output_tokens": 8192
                    }
                )
                return response.text
                
            except Exception as e:
                return f"⚠️ Gemini Error: {str(e)}"

        elif active_model == "openai":
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_query}]
            )
            return response.choices[0].message.content

        elif active_model == "perplexity":
            response = httpx.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "pplx-70b-online",
                    "messages": [{"role": "user", "content": full_query}]
                }
            )
            return response.json()["choices"][0]["message"]["content"]

        elif active_model == "groq":
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": full_query}]
            )
            return response.choices[0].message.content

        elif active_model == "deepseek":
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com/v1",
                default_headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": full_query}]
            )
            return response.choices[0].message.content

        else:
            return f"Unsupported model: {active_model}"

    except Exception as e:
        return f"⚠️ {active_model} Error: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🤖 Universal AI Assistant")
    
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Accordion("⚙️ Model Settings", open=False):
                model_selector = gr.Dropdown(
                    ["openai", "gemini", "claude", "perplexity", "groq", "deepseek"],
                    value=get_active_model(),
                    label="Active Model"
                )
                api_key = gr.Textbox(
                    label="API Key",
                    type="password",
                    value=get_api_key(get_active_model())
                )
                save_btn = gr.Button("Save Settings")
                status = gr.Textbox(label="Status", interactive=False)
        
        with gr.Column(scale=3):
            file_upload = gr.File(
                label="Upload Files",
                file_types=[".txt", ".pdf", ".docx", ".png", ".jpg", ".zip"],
                file_count="multiple"
            )
            input_box = gr.Textbox(label="Your Query", lines=3)
            submit_btn = gr.Button("Generate Response", variant="primary")
            output_box = gr.Textbox(label="Response", lines=10, interactive=False)

    model_selector.change(
        update_key_input,
        inputs=[model_selector],
        outputs=api_key
    )

    save_btn.click(
        save_settings_to_env,
        inputs=[model_selector, api_key],
        outputs=status
    )

    submit_btn.click(
        generate_response,
        inputs=[input_box, file_upload],
        outputs=output_box
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)