import time
import asyncio
import websockets
import threading

#---------------------------------------------------------------------------------------------------------

connected = set()
server_thread = None
DEBUG = False  # Set this flag to True to enable debug printing
DEFAULT_TIMEOUT = 1000 # 1 Second

# Create a global event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

#---------------------------------------------------------------------------------------------------------

def dprint(message):
    if DEBUG:
        print(message)

#---------------------------------------------------------------------------------------------------------

def extract_base_url (url):
    first_slash_pos = url.find("//") + 2
    second_slash_pos = url.find("/", first_slash_pos)
    return url[:second_slash_pos]    

#---------------------------------------------------------------------------------------------------------

def make_xpath (xpath):
    if not xpath.startswith(("/", "(")):
        xpath = f'//*[@id="{xpath}"]'
    return xpath

#---------------------------------------------------------------------------------------------------------

def wait_for_browser():
    global server_thread, connected
    if connected: return True

    if server_thread is None or not server_thread.is_alive():
        # Start the server thread if it doesn't exist or is not alive
        server_thread = threading.Thread (target=start_server)
        server_thread.daemon = True
        server_thread.start()
    
    while True:
        if not connected:
            dprint("Waiting for open website with Tampermonkey script...")
            time.sleep(1)
        else:
            dprint("Connected!")
            break
    return True

#---------------------------------------------------------------------------------------------------------

def send_command (cmd, tries = 0):
    if tries > 50:
        return "error"
    wait_for_browser()
    response = asyncio.run_coroutine_threadsafe (send_command_async (cmd), loop).result()
    if response is False:
        dprint ("Client disconnected. Resending command.")
        return send_command (cmd, tries = tries + 1)
    return response

#---------------------------------------------------------------------------------------------------------

async def send_command_async (cmd):
    if not connected:
        return False

    websocket = next (iter (connected))  # Get the first (and only) connected websocket
    try:
        # Send command
        await websocket.send(cmd)
        dprint(f"Sent command: {cmd}")
  
        # Wait for response
        response = await websocket.recv()
        dprint(f"Received response: {response}")
        return response

    except Exception:
        return False

#---------------------------------------------------------------------------------------------------------

async def handler (websocket, path):
    if len(connected) >= 1:
        await websocket.close()
        return
    client_ip = websocket.remote_address[0]
    connected.add(websocket)
    dprint(f"Connection from {client_ip}. Total connected: {len(connected)}")
    try:
        await websocket.wait_closed()  # Wait for the connection to close
        dprint(f"Connection with {client_ip} closed")
    except websockets.ConnectionClosed:
        dprint(f"Connection with {client_ip} closed")
    except Exception as e:
        dprint(f"Error handling connection: {e}")
    finally:
        if websocket in connected:
            connected.remove(websocket)  # Ensure the websocket is removed from the set
        dprint(f"Connection from {client_ip} removed. Total connected: {len(connected)}")

#---------------------------------------------------------------------------------------------------------

async def main():
    async with websockets.serve(handler, "127.0.0.1", 9999):
        dprint("WebSocket server started on ws://127.0.0.1:9999")
        await asyncio.Future()  # Run forever

#---------------------------------------------------------------------------------------------------------

def start_server():
    global loop
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

#---------------------------------------------------------------------------------------------------------

def goto_url (url):
    result = send_command (f"goto:{url}")
    if result == "error": return False
    return True

#---------------------------------------------------------------------------------------------------------

def wait_for (xpath, timeout = DEFAULT_TIMEOUT):
    xpath = make_xpath (xpath)
    result = send_command (f"wait_for:{xpath}|{timeout}")
    if result == "error": return False
    return result

#---------------------------------------------------------------------------------------------------------

def set_text(xpath, text, timeout = DEFAULT_TIMEOUT):
    xpath = make_xpath (xpath)
    result = send_command(f'set_text:{xpath}|{text}|{timeout}')
    if result != "success":
        return False
    return True

#---------------------------------------------------------------------------------------------------------

def run_js(js):
    result = send_command (f"js:{js}")
    if result == "error": return False
    return result

#---------------------------------------------------------------------------------------------------------

def click (xpath, timeout = DEFAULT_TIMEOUT):
    xpath = make_xpath (xpath)
    result = send_command (f'click:{xpath}|{timeout}')
    if result != "success": return False
    return True
