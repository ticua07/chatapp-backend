#!/usr/bin/env python
import asyncio
import json
from uuid import uuid4
from websockets import serve

from utils import ChatGroup

groups = []


async def echo(websocket, path):
    async for message in websocket:
        # TODO: Create chats, get 404 when chatID is not a ChatGroup
        # TODO: Get chats, maybe people too?
        # TODO: Delete chat when 0 people are available
        if not (len(groups) > 0):
            groups.append(
                {
                    # "id": uuid4().replace("-", ""),
                    "id": "1",
                    "group": ChatGroup("Chat 1", "Chat 1 only!!!"),
                }
            )
        converted_message = json.loads(message)
        converted_path = path[1:]
        match converted_message["type"]:
            case "connect":
                print("client has connected")
                for group in groups:
                    if group["id"] == converted_path:
                        await group["group"].Connect(websocket)

            case "newMessage":
                print("Got new message: " + converted_message["content"])
                for group in groups:
                    if group["id"] == converted_path:
                        await group["group"].SendMessage(
                            author=converted_message["author"],
                            message=converted_message["content"],
                        )

            case _:
                print("didn't understand nathing brooo")

    # Client closed website
    for group in groups:
        if group["id"] == converted_path:
            group["group"].Disconnect(websocket)


async def main():
    async with serve(echo, "0.0.0.0", 8765):
        print("Running on port 8765")
        await asyncio.Future()  # run forever


asyncio.run(main())
