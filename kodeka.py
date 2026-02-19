# cli/kodeka.py
import os
import sys
import json
import getpass
from pathlib import Path
from datetime import datetime

# Optional – comment out if not using
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import ollama
except ImportError:
    ollama = None

# Local modules
from history import ConversationHistory
from config import CONFIG_PATH, load_config, save_config, ensure_config_exists

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_provider_client(provider: str, api_key: str = None):
    provider = provider.lower()
    
    if provider == "ollama":
        if ollama is None:
            print("Error: 'ollama' python package not installed.")
            print("Run: pip install ollama")
            sys.exit(1)
        def ollama_chat(model, messages):
            response = ollama.chat(model=model, messages=messages)
            return response['message']['content']
        return ollama_chat, "llama3.2"  # default model
    
    elif provider == "openai":
        if OpenAI is None:
            print("Error: 'openai' package not installed.")
            print("Run: pip install openai")
            sys.exit(1)
        if not api_key:
            raise ValueError("OpenAI API key required")
        client = OpenAI(api_key=api_key)
        def openai_chat(model, messages):
            resp = client.chat.completions.create(
                model=model or "gpt-4o-mini",
                messages=messages
            )
            return resp.choices[0].message.content
        return openai_chat, "gpt-4o-mini"
    
    # Add more providers here later (groq, anthropic, gemini, deepseek...)
    
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def main():
    ensure_config_exists()
    config = load_config()

    # First-time setup
    if not config.get("provider"):
        clear_screen()
        print("┌────────────────────────────────────────────┐")
        print("│          Welcome to Kodeka CLI             │")
        print("│     First time setup – let's configure     │")
        print("└────────────────────────────────────────────┘\n")
        
        print("Available providers (that you have installed):")
        print("  • ollama     (local – recommended for privacy)")
        if OpenAI: print("  • openai     (needs API key)")
        print("  • (more coming soon: groq, anthropic, gemini...)")
        
        provider = input("\nChoose provider: ").strip().lower()
        api_key = ""
        
        if provider not in ["ollama"]:
            api_key = getpass.getpass(f"{provider.upper()} API key: ").strip()
        
        default_model = input("Model name (press Enter for default): ").strip() or None
        
        config.update({
            "provider": provider,
            "api_key": api_key,
            "model": default_model
        })
        save_config(config)
        print("\nConfiguration saved ✓\n")

    # Load conversation
    history = ConversationHistory("default")  # can be changed to username later

    # Get chat function
    try:
        chat_fn, default_model = get_provider_client(
            config["provider"],
            config.get("api_key")
        )
        model = config.get("model") or default_model
    except Exception as e:
        print(f"Error initializing provider: {e}")
        sys.exit(1)

    print(f"\nKodeka ({config['provider'].title()}) – model: {model}")
    print("  /help    /clear    /exit    /config\n")

    while True:
        try:
            user_input = input("You > ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input in ["/exit", "exit", "quit", ":q"]:
            print("Session ended.")
            break

        elif user_input == "/clear":
            history.clear()
            clear_screen()
            print("Conversation cleared.")
            continue

        elif user_input == "/help":
            print("""
Commands:
/help           – this help
/clear          – clear current conversation
/config         – show current configuration
/exit, quit     – exit the program
            """)
            continue

        elif user_input == "/config":
            print(json.dumps(config, indent=2))
            continue

        # Normal message
        history.add_user_message(user_input)

        try:
            messages = history.get_recent_history(max_messages=14)
            response = chat_fn(model, messages)
            print(f"\nKodeka: {response}\n")
            history.add_assistant_message(response)
        except Exception as e:
            print(f"\nError: {str(e)}\n")

if __name__ == "__main__":
    main()
