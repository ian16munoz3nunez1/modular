# Proyecto Modular (Equipo Amistad) 😉

## Archivos binarios

- [MicroPython](https://micropython.org/download/esp32)
- [esp32cam](https://github.com/lemariva/micropython-camera-driver)

## Librerias Python

- ***sockets*** `pip install sockets`
- ***opencv*** `pip install opencv-contrib-python`
- ***numpy*** `pip install numpy` 
- ***matplotlib*** `pip install matplotlib`
- ***thonny*** `pip install thonny-esp`
- ***pyserial*** `pip install pyserial`
- ***esptool*** `pip install esptool`
- ***ampy*** `pip install adafruit-ampy`

## Comandos y programas

### Windows

Listar los dispositivos conectados a los puertos:
`py -m serial.tools.list_ports`

Borrar la memoria del esp32:
`esptool.py --chip esp32 --port COM* erase_flash`

Cargar el archivo binario a la placa esp32:
`esptool.py --chip esp32 --port COM* --baud 460800 write_flash -z 0x1000 <esp32version>.bin`

Cargar un archivo *Python* a la esp32:
`ampy --port COM* put main.py`

Obtener el contenido de un archivo:
`ampy --port COM* get main.py`

Listar los archivos dentro de la placa:
`ampy --port COM* ls`

Crear conexión serial con la esp32 en PuTTY:

- Puerto: ***COM\****
- Velocidad: ***115200 bauds***

### Linux

Listar los dispositivos conectados a los puertos:
`python3 -m serial.tools.list_ports`

Borrar la memoria del esp32:
`esptool.py --chip esp32 --port /dev/ttyUSB* erase_flash`

Cargar el archivo binario a la placa esp32:
`esptool.py --chip esp32 --port /dev/ttyUSB* --baud 460800 write_flash -z 0x1000 <esp32version>.bin`

Cargar un archivo *Python* a la esp32:
`ampy --port /dev/ttyUSB* put main.py`

Obtener el contenido de un archivo:
`ampy --port /dev/ttyUSB* get main.py`

Listar los archivos dentro de la placa:
`ampy --port /dev/ttyUSB* ls`

Crear conexión serial con la esp32:
`picocom /dev/ttyUSB* -b 115200`

