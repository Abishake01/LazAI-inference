from alith.lazai import Client, ProofRequest
from alith.data import encrypt
from alith.data.storage import (
    PinataIPFS,
    UploadOptions,
    GetShareLinkOptions,
    StorageError,
)
from eth_account.messages import encode_defunct
from os import getenv
from dotenv import load_dotenv

load_dotenv()
import asyncio
import requests
import rsa
import aiohttp
from pydantic import BaseModel
from typing import Optional


class ActualPinataUploadResponse(BaseModel):
    id: str
    name: str
    cid: str
    size: int
    number_of_files: int
    mime_type: str
    created_at: str
    updated_at: str
    network: str
    streamable: bool
    # Optional fields that might not be present
    accept_duplicates: Optional[bool] = None
    is_duplicate: Optional[bool] = None
    group_id: Optional[str] = None


class CustomPinataIPFS(PinataIPFS):
    async def upload(self, opts: UploadOptions):
        url = "https://uploads.pinata.cloud/v3/files"

        form = aiohttp.FormData()
        form.add_field("file", opts.data, filename=opts.name, content_type="text/plain")
        form.add_field("network", "public")

        headers = {"Authorization": f"Bearer {opts.token}"}

        try:
            async with self.client.post(url, data=form, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise StorageError(f"Pinata IPFS API error: {error_text}")

                data = await response.json()
                # Use the actual response structure instead of the broken model
                pinata_response = ActualPinataUploadResponse(**data["data"])

                from alith.data.storage import FileMetadata
                return FileMetadata(
                    id=pinata_response.cid,
                    name=pinata_response.name,
                    size=pinata_response.size,
                    modified_time=pinata_response.updated_at,
                )
        except aiohttp.ClientError as e:
            raise StorageError(f"Network error: {str(e)}") from e


async def main():
    private_key = getenv("PRIVATE_KEY")
    if not private_key:
        raise ValueError(
            "PRIVATE_KEY environment variable is required. Set it in your shell or in a .env file."
        )

    client = Client(private_key=private_key)
    ipfs = CustomPinataIPFS()  # Use our custom implementation
    try:
        # 1. Prepare your privacy data and encrypt it
        data_file_name = "my_self_intro.txt"
        privacy_data = """
      Name / nickname: Abishake — I prefer to be called Abi.

I’m a full-stack developer who enjoys building end-to-end projects solo (backend → frontend).

Tech stack & interests: Python, Django, React, Tailwind CSS, MySQL, and I often work with AI, Web3, smart contracts, and voice/agent systems.

Current projects / goals mentioned:

AI blog generator in Django (generates posts from YouTube links).

Netflix clone in Django (Tailwind CSS).

Web3 app “Devma” (hackathon/events), dark UI + multicolor gradients.

Video call website in Django.

AI Lawyer for Indian users (React/TypeScript frontend + Python backend), responses concise (5–8 lines) and Tanglish speech option.

Agriculture AI assistant (crop recommendations, well drainage estimation, 3D well model).

FIR registration & tracking platform (IPFS, biometric/Aadhaar validation, ai-lawyer-agent).

POS billing site in React (auth, billing, reports).

Inventory Management System (React + TypeScript + Supabase, want Google Drive storage).

Many other ideas: Python→Rust converter, birthday wish website, EdTech platform, AI agents, etc.

Teaching: I run weekly Python full-stack classes at college (20–40 students) and enjoy teaching beginners.

I’ve worked on / asked about: connecting Django to MySQL on Railway, deploying on Render, Swagger for Django API, React Native + Django backend, integrating AI models into Flask, using Groq and Alith/LazAI, DAT token and LazAI concepts, and many tutorial-style posts.

Recent activity: I posted a Medium article titled “Harnessing LazAI with Alith: A Step-by-Step Guide to Accessing and Using the Alith Framework with a Free API Key” (includes Python example). I wanted the article to sound more natural and interactive (not overly AI-generated).

Personal preferences / style: I like interactive, natural, conversational blog tone (Abi-style), and prefer content that doesn’t read like it was written by an AI. I enjoy clean UI/UX, animations, and making projects visually appealing.

Course & curriculum preferences: I created an 8-week Full-Stack course covering HTML/CSS/Bootstrap/JS, React + Spring Boot + MySQL, Django + MySQL, and MERN. Classes are 3 days/week with daily tasks and a weekly task.

Misc technical preferences: I prefer Python 3.8+, virtual envs, using .env for secrets, and practical, example-driven tutorials.

I’ve given me many project-specific requests and code snippets across 2024–2025 (details stored as conversation history and project notes).
        """
        
        
        encryption_seed = "Sign to retrieve your encryption key"
        message = encode_defunct(text=encryption_seed)
        password = client.wallet.sign_message(message).signature.hex()
        encrypted_data = encrypt(privacy_data.encode(), password)
        # 2. Upload the privacy data to IPFS and get the shared url
        token = getenv("IPFS_JWT", "")
        file_meta = await ipfs.upload(
            UploadOptions(name=data_file_name, data=encrypted_data, token=token)
        )
        url = await ipfs.get_share_link(
            GetShareLinkOptions(token=token, id=file_meta.id)
        )
        # 3. Upload the privacy url to LazAI (print tx hash first, then file id)
        file_id = client.get_file_id_by_url(url)
        if file_id == 0:
            try:
                res = client.add_file_tx(url)
                # Ensure 0x prefix on tx hash
                tx_hash = res["tx_hash"]
                if not tx_hash.startswith("0x"):
                    tx_hash = f"0x{tx_hash}"
                print("Tx Hash:", tx_hash)
                file_id = res["file_id"]
                
            except Exception:
                # Fallback if add_file_tx not available
                tx_hash = None
                file_id = client.add_file(url)
                print("File ID:", file_id)
        else:
            print("File ID:", file_id)
        # 4. Request proof in the verified computing node
        client.request_proof(file_id, 100)
        job_id = client.file_job_ids(file_id)[-1]
        job = client.get_job(job_id)
        node_info = client.get_node(job[-1])
        node_url: str = node_info[1]
        pub_key = node_info[-1]
        encryption_key = rsa.encrypt(
            password.encode(),
            rsa.PublicKey.load_pkcs1(pub_key.strip().encode(), format="PEM"),
        ).hex()
        response = requests.post(
            f"{node_url}/proof",
            json=ProofRequest(
                job_id=job_id,
                file_id=file_id,
                file_url=url,
                encryption_key=encryption_key,
                encryption_seed=encryption_seed,
                proof_url=None,
            ).model_dump(),
        )
        if response.status_code == 200:
            print("Proof request sent successfully")
        else:
            print("Failed to send proof request:", response.json())
        # 5. Request DAT reward
        client.request_reward(file_id)
        print("Reward requested for file id", file_id)
    except StorageError as e:
        print(f"Error: {e}")
    except Exception as e:
        raise e
    finally:
        await ipfs.close()


if __name__ == "__main__":
    asyncio.run(main())
