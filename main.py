#!/usr/bin/env python
import asyncio
import json
from uuid import uuid4
from websockets import serve

from utils import ChatGroup

groups = []


async def echo(websocket, path):
    async for message in websocket:
        converted_message = json.loads(message)
        converted_path = path[1:]
        if converted_path == "chat":
            match converted_message["type"]:
                case "create":
                    print("User is trying to create a new chat")
                    chatID = str(uuid4()).replace("-", "")
                    groups.append(
                        {
                            "id": chatID,
                            "group": ChatGroup(
                                title=converted_message["title"],
                                description=converted_message["description"],
                            ),
                        }
                    )
                    await websocket.send(
                        json.dumps({"type": "created", "chatID": chatID})
                    )

                case "getChats":
                    data = [
                        {"id": i["id"], "groupData": i["group"].GetGroupData()}
                        for i in groups
                    ]
                    await websocket.send(json.dumps({"type": "chatlist", "data": data}))

        # TODO: Create chats, get 404 when chatID is not a ChatGroup
        # TODO: Delete chat when 0 people are available

        print(f"converted path is {converted_path} and message is {message}")
        match converted_message["type"]:
            case "connect":
                print("client has connected")
                successful = False
                for group in groups:
                    if group["id"] == converted_path:
                        await group["group"].Connect(websocket)
                        successful = True

                if not successful:
                    print("not connected")
                    await websocket.send(
                        json.dumps({"type": "error404", "message": "go back to lobby"})
                    )

            case "newMessage":
                print("Got new message: " + converted_message["content"])
                successful = False

                for group in groups:
                    if group["id"] == converted_path:
                        await group["group"].SendMessage(
                            author=converted_message["author"],
                            message=converted_message["content"],
                        )
                        successful = True

                if not successful:
                    print("not sent")
                    await websocket.send(
                        json.dumps({"type": "error404", "message": "go back to lobby"})
                    )

    # Client closed website
    for group in groups:
        if group["id"] == converted_path:
            group["group"].Disconnect(websocket)


async def main():
    async with serve(echo, "0.0.0.0", 8765):
        print("Running on port 8765")
        await asyncio.Future()  # run forever


try:
    asyncio.run(main())
except:
    print("Exiting...")
