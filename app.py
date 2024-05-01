import tkinter as tk
import tkinter.ttk as ttk
from serial import Serial, SerialException
from serial.tools.list_ports import comports
from tkinter.messagebox import showerror
from threading import Thread, Lock

S_OK = 0xaa
S_ERR = 0xff

def detached_callback(f):
    return lambda *args, **kwargs: Thread(target=f, args=args, kwargs=kwargs).start()

class SerialPortal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.withdraw()
        ttk.OptionMenu(self, self.parent.port, '', *[d.device for d in comports()]).pack()
        ttk.Button(self, text='Connect', command=self.connect, default='active').pack()

    def connect(self):
        self.parent.connect()
        self.destroy()
        self.parent.deiconify()

class App(tk.Tk):
    ser: Serial

    def __init__(self):
        super().__init__()
        self.title("LED Blinker")
        self.port = tk.StringVar()
        self.led = tk.BooleanVar()

        ttk.Checkbutton(self, text='Toggle LED', variable=self.led, command=self.update_led).pack()
        ttk.Button(self, text='Send Invalid', command=self.send_invalid).pack()
        ttk.Button(self, text='Disconnect', command=self.disconnect, default='active').pack()
        SerialPortal(self)

    def connect(self):
        self.ser = Serial(self.port.get())

    def write(self, b: bytes):
        try:
            self.ser.write(b)
            if int.from_bytes(self.ser.read(), 'big') != S_OK:
                showerror('Device Error', 'The device reported an error.')
        except SerialException:
            showerror('Serial Error', 'Communication error.')

    @detached_callback
    def update_led(self):
        self.write(bytes([int(self.led.get())]))

    def send_invalid(self):
        self.write(bytes([0x10]))

    def disconnect(self):
        if self.ser.is_open:
            self.ser.close()
        SerialPortal(self)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.disconnect()

class LockedSerial(Serial):
    _lock: Lock = Lock()

    def read(self, size=1) -> bytes:
        with self._lock:
            return super().read(size)

    def write(self, b: bytes, /) -> int:
        with self._lock:
            return super().write(b)

    def close(self):
        with self._lock:
            super().close()

if __name__ == '__main__':
    with App() as app:
        app.mainloop()

