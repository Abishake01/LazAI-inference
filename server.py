from alith.inference import run
 
# Example: Using DeepSeek model from OpenRouter
server = run(settlement=True, engine_type="openai", model="deepseek/deepseek-chat-v3.1:free")