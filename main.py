import binascii

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src import SerialBuilder
from src import MessageBuilder
from src import MessageCommands, MessageAreas

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/send_config")
async def send_data(request: Request):
    data = await request.json()

    com_port = data.get("comPort", "COM3")
    baudrate = data.get("baudrate", "115200")

    app.serial = (SerialBuilder.read_configuration()
                                   .update_port(com_port)
                                   .update_baudrate(baudrate)
                                   .build())
    
    app.serial.open_serial_port()
    app.serial.flush()
    
    
@app.post("/send_message")
async def send_data(request: Request):
    data = await request.json()

    command = bytes.fromhex(data.get("command", ""))
    mem_area = bytes.fromhex(data.get("mem_area", "").zfill(2))
    if command == MessageCommands.WRITE:
        data_command = bytes.fromhex(data.get("data", "FF").zfill(2))
    else:
        data_command = b'\xFF'

    message = (MessageBuilder.set_memory_area(mem_area)
                             .set_command(command)
                             .set_data(data_command)
                             .build())
    
    if hasattr(app, 'serial'):
        app.serial.send_byte_stream(message.byte_stream)
        return_message = app.serial.read_byte_stream()
        if command == MessageCommands.READ:
            if b'ACKOK' in return_message:
                try:
                    hex_string = return_message.decode('utf-8')
                    updated_content = hex_string.split("ACKOK")[0]
                    print(hex_string) 
                except:
                    hex_string = binascii.hexlify(return_message).decode('utf-8').upper()
                    updated_content = hex_string.replace('0', '').replace("41434B4F4B", '')

                return JSONResponse(content={"updatedContent": updated_content})


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Route to handle requests to the root endpoint.

    Parameters:
    - request (fastapi.Request): The incoming HTTP request.

    Returns:
    - fastapi.responses.HTMLResponse: An HTML response rendered using Jinja2 templates.
    """
    
    return templates.TemplateResponse("index.html", {"request": request})