# server.py
import asyncio
import websockets

connected_clients = set()

async def handler(websocket):
    print("New client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print("Received:", message)
            # Broadcast to all other clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Server started on port 8765")
        await asyncio.Future()  # run forever

asyncio.run(main())