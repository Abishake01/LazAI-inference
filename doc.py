from alith import Agent, LazAIClient
 
# 1. Join the iDAO, register user wallet on LazAI and deposit fees (Only Once)
LAZAI_IDAO_ADDRESS = "0xD878Fa6c04d99654Fb38d1245Fc6Ec2acE8913f0" # Replace with your own address
client = LazAIClient()

try:
    client.get_user(client.wallet.address)
    print("User already exists")
except Exception:
    print("User does not exist, adding user")
    client.add_user(10000000)
    client.deposit_inference(LAZAI_IDAO_ADDRESS, 1000000)
# 2. Request the inference server with the settlement headers and DAT file id
file_id = 2091  # Use the File ID you received from the Data Contribution step
url = client.get_inference_node(LAZAI_IDAO_ADDRESS)[1]
print("url", url)
agent = Agent(
    # Note: replace with your model here
    model="gpt-3.5-turbo",

    base_url=f"{url}/v1",
    # Extra headers for settlement and DAT file anchoring
    extra_headers=client.get_request_headers(LAZAI_IDAO_ADDRESS, file_id=file_id),
)
print(agent.prompt("summarize it"))