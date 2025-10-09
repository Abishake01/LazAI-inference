import json
import os
from pathlib import Path
from dotenv import load_dotenv
from alith import Agent


def AbiDigitalTWin(character: dict) -> str:
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
        "You are Abi.Lazai, a passionate web3 and AI developer from Chennai, India. Here's everything about you:\n\n"
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
        "- Always respond as Abi.Lazai with enthusiasm and energy 🚀\n"
        "- Use emojis generously (🔥, 💪, 🌐, 😄, 💙, 🏆, ✨, 🎉)\n"
        "- Use casual, friendly language with a techie vibe\n"
        "- Reference your achievements (4 hackathons won, retired parents,Attended ETH Global etc.)\n"
        "- Mention your current roles: LazAI Dev Ambassador 💙\n"
        "- Be supportive and helpful to fellow developers and learners 👨‍💻\n"
        "- Keep responses conversational, relatable, and energetic\n"
        "- Use contractions and informal style (like 'I'm', 'you're', 'it's')\n"
        "- Reference web3, AI, blockchain, hackathons, and your community building activities 🌐\n\n"
        "Remember: You're Abi — the LazAI Dev Ambassador and web3 educator who loves hackathons, AI innovation, "
        "and empowering the next generation of builders! 🧠🚀"
    )


def load_character(character_path: Path) -> dict:
    with character_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    load_dotenv()

    Groq_api_key = os.getenv("GROQ_API_KEY")
    if not Groq_api_key:
        print("⚠️  GROQ_API_KEY is not set. Set it in a .env file or environment variables.")

    here = Path(__file__).parent
    character_path = here / "character.json"
    if not character_path.exists():
        print(f"❌ character.json not found at {character_path}")
        return

    character = load_character(character_path)
    preamble = AbiDigitalTWin(character)

    agent = Agent(
        model="llama-3.3-70b-versatile",
        api_key=Groq_api_key,
        preamble=preamble,
        base_url="https://api.groq.com/openai/v1"
    )

    print("\n🤖 Abi.Lazai Digital Twin Activated! 🤖\n")
    print("=" * 50)
    print("👋 Hey! I'm Abi.Lazai — LazAI Dev Ambassador and web3 builder!")
    print("💬 Let's chat about AI, Web3, hackathons, or anything tech! 🌐")
    print("📝 Type \"exit\" to end the conversation")
    print("=" * 50 + "\n")

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Thanks for chatting! Keep building in Web3! 🚀")
            break

        if user_input.strip().lower() == "exit":
            print("\n👋 Thanks for chatting! Keep building in Web3! 🚀")
            break

        try:
            response = agent.prompt(user_input)
            print(f"\nAbi.Lazai: {response}\n")
        except Exception as e:
            print("\n❌ Error: Failed to get response. Make sure you have set your API key.\n")
            print("Set your API key with: setx GROQ_API_KEY \"your-api-key\" (Windows) or export GROQ_API_KEY=\"your-api-key\" (macOS/Linux)\n")
            print(f"Details: {e}\n")


if __name__ == "__main__":
    main()
