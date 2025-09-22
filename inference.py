from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from alith import Agent, LazAIClient

load_dotenv()

# 1. Join the iDAO, register user wallet on LazAI and deposit fees (Only Once)
LAZAI_IDAO_ADDRESS = "0xD878Fa6c04d99654Fb38d1245Fc6Ec2acE8913f0" 

private_key = getenv("PRIVATE_KEY")
if not private_key:
    raise ValueError("PRIVATE_KEY environment variable is required")

client = LazAIClient(private_key=private_key,)
# Add by the inference node admin

# Use a smaller deposit amount to avoid overflow
DEPOSIT_AMOUNT = 1000000  # Reduced from 10000000

print(f"Using wallet address: {client.wallet.address}")

try:
    address = client.get_user(client.wallet.address)
    print("User already exists", address)
    # client.deposit_inference(LAZAI_IDAO_ADDRESS, DEPOSIT_AMOUNT)

except Exception:
    print("User does not exist, adding user")
    try:
        client.add_user(DEPOSIT_AMOUNT)
        client.deposit(DEPOSIT_AMOUNT * 2)
        print("Deposit successful")
        client.deposit_inference(LAZAI_IDAO_ADDRESS, DEPOSIT_AMOUNT)
        print(f"Successfully added user and deposited {DEPOSIT_AMOUNT}")
    except Exception as e:
        print("Error adding user or depositing:", e)

# 2. Request the inference server with the settlement headers and DAT file id
# Read FILE_ID from environment, else fall back to local file written by Dat.py
file_id_str = getenv("FILE_ID")
if not file_id_str:
    fid_path = Path(__file__).with_name("file_id.txt")
    if fid_path.exists():
        try:
            file_id_str = fid_path.read_text(encoding="utf-8").strip()
        except Exception as e:
            raise RuntimeError(f"Failed to read {fid_path.name}: {e}")
if not file_id_str:
    raise ValueError(
        "FILE_ID is not set. Set FILE_ID in your environment or run Dat.py first to create file_id.txt."
    )
try:
    file_id = int(file_id_str)
except ValueError:
    raise ValueError(f"Invalid FILE_ID '{file_id_str}'. Must be an integer.")

url = client.get_inference_node(LAZAI_IDAO_ADDRESS)[1]
print("url", url)

# Check if the user has an account with the inference node
try:
    account = client.get_inference_account(client.wallet.address, LAZAI_IDAO_ADDRESS)
    print("Inference account:", account)
    if not account or account[0] != client.wallet.address:
        print("Warning: User account not found with inference node. This may cause authentication errors.")
except Exception as e:
    print("Error checking inference account:", e)

groq_api_key = getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is required for the selected model.")

agent = Agent(
    # Note: replace with your model here
    model="llama-3.3-70b-versatile",
    api_key=groq_api_key,
    # OpenAI-compatible inference server URL
    base_url=f"{url}/v1",
    
    # Extra headers for settlement and DAT file anchoring
    extra_headers=client.get_request_headers(LAZAI_IDAO_ADDRESS, file_id=file_id),
)
print(agent.prompt("Write a poem about LazAI and decentralized AI inference."))