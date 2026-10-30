import os
import requests

message = {
    "content": "🚀 Scanner is running successfully!"
}

requests.post(
    os.getenv("DISCORD_WEBHOOK_URL"),
    json=message
)

print("DISCORD MESSAGE SENT")
