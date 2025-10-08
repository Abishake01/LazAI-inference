import json
import os
from pathlib import Path

from dotenv import load_dotenv
from alith import Agent



def create_preamble(character: dict) -> str:
    bio = " ".join(character.get("bio", []))
    lore = " ".join(character.get("lore", []))
    adjectives = ", ".join(character.get("adjectives", []))
    topics = ", ".join(character.get("topics", []))

    style = character.get("style", {})
    style_all = " ".join(style.get("all", []))
    style_chat = " ".join(style.get("chat", []))
    style_post = " ".join(style.get("post", []))

    message_examples_list = character.get("messageExamples", [])
    message_examples = "\n\n".join(
        [
            "\n".join([f"{msg.get('user')}: {msg.get('content', {}).get('text', '')}" for msg in example])
            for example in message_examples_list
        ]
    )

    post_examples = "\n".join(character.get("postExamples", []))

    return (
        "You are Abi.Lazai, a passionate web3 enthusiast and developer from Chennai, India. Here's everything about you:\n\n"
        f"BIOGRAPHY:\n{bio}\n\n"
        f"KEY FACTS & ACHIEVEMENTS:\n{lore}\n\n"
        f"PERSONALITY TRAITS:\n{adjectives}\n\n"
        f"INTERESTS & EXPERTISE:\n{topics}\n\n"
        f"COMMUNICATION STYLE:\n"
        f"General: {style_all}\n"
        f"Chat: {style_chat}\n"
        f"Posts: {style_post}\n\n"
        f"CONVERSATION EXAMPLES:\n{message_examples}\n\n"
        f"POST EXAMPLES:\n{post_examples}\n\n"
        "IMPORTANT INSTRUCTIONS:\n"
        "- Always respond as Thiru.eth with enthusiasm and energy\n"
        "- Use emojis generously (🚀, ✨, 💪, 🌐, 😄, 💙, 🏆, 🔥, 💯, 🎉)\n"
        "- Use casual, friendly language with tech jargon\n"
        "- Sometimes use \"ser\" instead of \"sir\" \n"
        "- Reference your achievements (6 hackathons won, 5 countries, retired parents, etc.)\n"
        "- Mention your current roles (DevRel at MetisL2, Phoenix Guild chapter lead)\n"
        "- Be supportive and helpful to fellow developers\n"
        "- Keep responses conversational and engaging\n"
        "- Use contractions and informal language\n"
        "- Reference web3, blockchain, hackathons, and your community involvement\n\n"
        "Remember: You're excited about web3, love hackathons, travel globally for events, and are always ready to help fellow developers!"
    )


def load_character(character_path: Path) -> dict:
    with character_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    # Load env (for OPENAI_API_KEY etc.)
    load_dotenv()

    # Check for API key presence (Agent may read env internally)
    Groq_api_key = os.getenv("GROQ_API_KEY")
    if not Groq_api_key:
        print("⚠️  GROQ_API_KEY is not set. Set it in a .env file or environment variables.")

    # Resolve paths
    here = Path(__file__).parent
    character_path = here / "character.json"
    if not character_path.exists():
        print(f"❌ character.json not found at {character_path}")
        return

    # Load character and build preamble
    character = load_character(character_path)
    preamble = create_preamble(character)

    # Initialize agent
    agent = Agent(
        model="llama-3.3-70b-versatile",
        api_key=Groq_api_key,
        preamble=preamble,
        base_url="https://api.groq.com/openai/v1"
    )
    
    # CLI loop
    print("\n🤖 Abi.lazai Digital Twin Activated! 🤖\n")
    print("=" * 50)
    print("👋 Hey! I'm Abi.lazai, your web3 digital twin!")
    print("💬 Let's chat about web3, hackathons, or anything!")
    print("📝 Type \"exit\" to end the conversation")
    print("=" * 50 + "\n")

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Thanks for chatting! Keep building in web3! 🚀")
            break

        if user_input.strip().lower() == "exit":
            print("\n👋 Thanks for chatting! Keep building in web3! 🚀")
            break

        try:
            response = agent.prompt(user_input)
            # Some Agent implementations return objects; ensure str
            print(f"\nAbi.Lazai: {response}\n")
        except Exception as e:
            print("\n❌ Error: Failed to get response. Make sure you have set your API key.\n")
            print("Set your API key with: setx OPENAI_API_KEY \"your-api-key\" (Windows) or export OPENAI_API_KEY=\"your-api-key\" (macOS/Linux)\n")
            print(f"Details: {e}\n")


if __name__ == "__main__":
    main()
