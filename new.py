from alith import Agent, LazAIClient

# 1. Join the iDAO, register user wallet on LazAI and deposit fees (Only Once)
LAZAI_IDAO_ADDRESS = "0xD878Fa6c04d99654Fb38d1245Fc6Ec2acE8913f0" # Replace with your own address

client = LazAIClient()
# Add by the inference node admin

client.deposit_inference(LAZAI_IDAO_ADDRESS, 1000000)
DEPOSIT_AMOUNT = 1000000  
 
 

try:
    client.get_user(client.wallet.address)
    print("User already exists")
    address = client.get_user(client.wallet.address)
    
    print("User already exists", address)
  
 
except Exception:
    print("User does not exist, adding user")
    client.add_user(10000000)
    try:
        client.add_user(DEPOSIT_AMOUNT)
        client.deposit(DEPOSIT_AMOUNT * 2)
        client.deposit_inference(LAZAI_IDAO_ADDRESS, DEPOSIT_AMOUNT)
        print(f"Successfully added user and deposited {DEPOSIT_AMOUNT}")
    except Exception as e:
        print("Error adding user or depositing:", e)
 

# 2. Request the inference server with the settlement headers and DAT file id
file_id = 10  # Use the File ID you received from the Data Contribution step
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
 
agent = Agent(
    # Note: replace with your model here
    model="deepseek/deepseek-r1-0528",
    # OpenAI-compatible inference server URL
    base_url=f"{url}/v1",
    # Extra headers for settlement and DAT file anchoring
    extra_headers=client.get_request_headers(LAZAI_IDAO_ADDRESS, file_id=file_id),
)
print(agent.prompt("summarize it"))