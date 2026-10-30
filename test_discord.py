import os
import requests

webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

message = {
    "content": "✅ Smart Money Scanner Connected Successfully!"
}

requests.post(webhook_url, json=message)

print("Message sent")
