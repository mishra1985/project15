import json
import re
import time
import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from accounts.models import ChatMessage
import os
# Replace with your actual Gemini API key.
GEMINI_API_KEY = os.environ.get('GENERATIVE_AI_API_KEY')
# Streaming endpoint for Gemini content generation.
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?alt=sse&key={GEMINI_API_KEY}"

def clean_text(text):
    """
    Cleans the text by removing markdown formatting and extra whitespace.
    """
    text = re.sub(r'(\*\*|\*)', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@sync_to_async
def save_chat_message(username, message, time_taken=None):
    # Save the message and return the created ChatMessage instance.
    return ChatMessage.objects.create(username=username, message=message, time_taken=time_taken)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print("WebSocket connection accepted")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get("username", "Anonymous")
        prompt = data.get("message", "")

        # Save and broadcast the user's message.
        user_message_obj = await save_chat_message(username, prompt)
        await self.send(text_data=json.dumps({
            "username": username,
            "message": prompt,
            "timestamp": user_message_obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }))

        # Record the start time for Gemini reply.
        start_time = time.monotonic()

        # Retrieve the aggregated Gemini response.
        aggregated_response = await self.get_aggregated_gemini_response(prompt)
        truncated_response = clean_text(aggregated_response)
        # Calculate time taken.
        end_time = time.monotonic()
        duration = end_time - start_time

        # Save the Gemini message.
        gemini_message_obj = await save_chat_message("Gemini", truncated_response, time_taken=duration)

        # Broadcast the Gemini response (with timestamp and time taken).
        await self.send(text_data=json.dumps({
            "username": "Gemini",
            "message": truncated_response,
            "timestamp": gemini_message_obj.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "time_taken": f"{duration:.2f} sec"
        }))

    async def get_aggregated_gemini_response(self, prompt):
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        aggregated = ""
        async with aiohttp.ClientSession() as session:
            async with session.post(GEMINI_API_URL, json=payload, headers=headers) as resp:
                async for line_bytes in resp.content:
                    line = line_bytes.decode("utf-8").strip()
                    if line.startswith("data:"):
                        data_str = line[5:].strip()  # Remove "data:" prefix.
                        if data_str:
                            try:
                                data = json.loads(data_str)
                                if "candidates" in data and data["candidates"]:
                                    candidate = data["candidates"][0]
                                    content = candidate.get("content", {})
                                    parts = content.get("parts", [])
                                    if parts and "text" in parts[0]:
                                        aggregated += parts[0]["text"] + " "
                                    if candidate.get("finishReason") == "STOP":
                                        break
                            except Exception as e:
                                print("Error processing SSE line:", e)
        return aggregated
