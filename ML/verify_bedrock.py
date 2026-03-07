"""
Quick diagnostic script to verify AWS Bedrock access and model availability
"""
import boto3
import os
from dotenv import load_dotenv
from botocore.config import Config

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = "us.amazon.nova-2-lite-v1:0"

print("=" * 70)
print("AWS BEDROCK DIAGNOSTIC CHECK")
print("=" * 70)

# Check environment variables
print("\n1. ENVIRONMENT VARIABLES:")
print(f"   AWS_REGION: {AWS_REGION}")
print(f"   AWS_ACCESS_KEY_ID: {'✓ Set' if os.getenv('AWS_ACCESS_KEY_ID') else '✗ Missing'}")
print(f"   AWS_SECRET_ACCESS_KEY: {'✓ Set' if os.getenv('AWS_SECRET_ACCESS_KEY') else '✗ Missing'}")
print(f"   AWS_SESSION_TOKEN: {'✓ Set' if os.getenv('AWS_SESSION_TOKEN') else '○ Not set (optional)'}")

# Try to create client
print("\n2. BOTO3 CLIENT:")
try:
    client_kwargs = {
        "service_name": "bedrock-runtime",
        "region_name": AWS_REGION,
        "config": Config(read_timeout=60, connect_timeout=30),
    }
    
    if os.getenv("AWS_ACCESS_KEY_ID"):
        client_kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID")
    if os.getenv("AWS_SECRET_ACCESS_KEY"):
        client_kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY")
    if os.getenv("AWS_SESSION_TOKEN"):
        client_kwargs["aws_session_token"] = os.getenv("AWS_SESSION_TOKEN")
    
    client = boto3.client(**client_kwargs)
    print(f"   ✓ Bedrock Runtime client created successfully")
except Exception as e:
    print(f"   ✗ Failed to create client: {e}")
    exit(1)

# Try a simple text-only request
print("\n3. BASIC TEXT REQUEST:")
try:
    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": "Reply with just 'OK' if you can read this."}],
            }
        ],
        inferenceConfig={"maxTokens": 10, "temperature": 0.7},
    )
    
    text = response["output"]["message"]["content"][0]["text"]
    print(f"   ✓ Model responded: {text}")
    print(f"   ✓ Model is accessible and working!")
except Exception as e:
    print(f"   ✗ Request failed: {e}")
    print(f"\n   Possible issues:")
    print(f"   - Model not enabled in AWS account")
    print(f"   - Insufficient permissions (need bedrock:InvokeModel)")
    print(f"   - Wrong region (Nova might not be available in {AWS_REGION})")
    print(f"   - Invalid credentials")
    exit(1)

# Try image request
print("\n4. MULTIMODAL (IMAGE) REQUEST:")
try:
    # Create a tiny test image
    from PIL import Image
    import io
    
    img = Image.new('RGB', (100, 100), color='red')
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    image_bytes = buf.getvalue()
    
    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "image": {
                            "format": "jpeg",
                            "source": {"bytes": image_bytes},
                        }
                    },
                    {"text": "What color is this image? Reply in one word."},
                ],
            }
        ],
        inferenceConfig={"maxTokens": 20, "temperature": 0.7},
    )
    
    text = response["output"]["message"]["content"][0]["text"]
    print(f"   ✓ Multimodal response: {text}")
    print(f"   ✓ Image processing is working!")
except Exception as e:
    print(f"   ✗ Multimodal request failed: {e}")
    import traceback
    print(f"\n   Full traceback:")
    print(traceback.format_exc())
    exit(1)

print("\n" + "=" * 70)
print("✓ ALL CHECKS PASSED - Bedrock is configured correctly!")
print("=" * 70)
