from dataclasses import dataclass
import threading
import ctypes
import win32api
import win32gui
import os
import get_data

# clear terminal screen
os.system('cls')

class Clipboard:
    def _create_window(self) -> int:
        """
        Create a window for listening to messagesno
        :return: window hwnd
        """
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._process_message
        wc.lpszClassName = self.__class__.__name__
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        return win32gui.CreateWindow(class_atom, self.__class__.__name__, 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)

    def _process_message(self, hwnd: int, msg: int, wparam: int, lparam: int):
        WM_CLIPBOARDUPDATE = 0x031D
        if msg == WM_CLIPBOARDUPDATE:
            print('Clipboard saturs ir jaunināts!')
            get_data.write_tempfile()
            get_data.get_data()
            get_data.write_logfile()
            get_data.fill_form()
        return 0

    def listen(self):
        def runner():
            hwnd = self._create_window()
            ctypes.windll.user32.AddClipboardFormatListener(hwnd)
            win32gui.PumpMessages()

        th = threading.Thread(target=runner, daemon=True)
        th.start()
        while th.is_alive():
            th.join(0.25)

if __name__ == '__main__':
    clipboard = Clipboard()
    clipboard.listen()
