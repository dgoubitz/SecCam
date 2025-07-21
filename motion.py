from main import start_detection, motion_detected  # Assuming same directory


import asyncio
import websockets
import json
from constants import TOKEN


HA_URL = "ws://192.168.1.108:8123/api/websocket"
# TOKEN = "your_long_lived_access_token"

async def listen_motion():
    async with websockets.connect(HA_URL) as websocket:
        await websocket.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        auth_response = await websocket.recv()
        print("Auth:", auth_response)

        await websocket.send(json.dumps({
            "id": 1,
            "type": "subscribe_events",
            "event_type": "state_changed"
        }))

        while True:
            message = await websocket.recv()
            data = json.loads(message)

            if data.get("event") and data["event"]["event_type"] == "state_changed":
                entity_id = data["event"]["data"]["entity_id"]
                if "motion_sensor" in entity_id:
                    new_state = data["event"]["data"]["new_state"]["state"]
                    print(f"{entity_id} is now {new_state}")
                    
                    # Inside your motion handling:
                    if new_state == "on":
                        print("Motion detected, starting detection")
                        motion_detected = True
                        start_detection()  # starts the image capture
                    elif new_state == "off":
                        print("Motion stopped")
                        motion_detected = False

asyncio.run(listen_motion())