import json
from uuid import uuid4


class ChatGroup:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        self.connected = []
        self.messages = []

    def GetGroupData(self):
        return {
            "title": self.title,
            "description": self.description,
            "connected": len(self.connected),
        }

    def GetMessages(self, lastN):
        last_messages = self.messages[len(self.messages) - lastN : len(self.messages)]
        return last_messages

    async def SendMessage(self, author, message):
        print(f"sending to {len(self.connected)} people")
        new_message = {"author": author, "content": message}
        self.messages.append(new_message)
        for conn in self.connected:
            await conn["socket"].send(json.dumps(new_message | {"type": "newMessage"}))

    async def Connect(self, ws):
        randomIdentifier = str(uuid4()).split("-")[0]
        self.connected.append({"socket": ws, "id": randomIdentifier})
        # self.connected.append(ws)
        await ws.send(json.dumps({"type": "identify", "randomID": randomIdentifier}))

    def Disconnect(self, ws):
        try:
            # self.connected.remove(ws)
            print(f"previous member (removing) {len(self.connected)}")
            for conn in self.connected:
                if conn["socket"] == ws:
                    self.connected.remove(conn)
                    print("ChatGroup member has disconnected")

            print(f"after members (removing) {len(self.connected)}")
        except ValueError:
            print("couldn't remove websocket")
