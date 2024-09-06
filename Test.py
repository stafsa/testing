import ctypes
import time
import requests
import multiprocessing
from io import BytesIO
from PIL import Image
from win32api import GetSystemMetrics, Sleep
from win32con import SRCCOPY, PATINVERT
from win32gui import GetDC, CreateCompatibleDC, CreateCompatibleBitmap, SelectObject, BitBlt, DeleteObject, DeleteDC
import random
import win32gui

# Define ANTIALIAS for image processing
ANTIALIAS = Image.ANTIALIAS

# Constants for screen dimensions
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


# Melting Screen Effect
def melting_screen_effect():
    hdc = win32gui.GetDC(0)
    while True:
        x = random.randint(0, sw)
        win32gui.BitBlt(hdc, x, 1, 10, sh, hdc, x, 0, SRCCOPY)
        win32gui.ReleaseDC(0, hdc)
        Sleep(50)


# Rounded Tunnel Effect
def rounded_tunnel_effect():
    screen_size = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
    left, top, right, bottom = screen_size

    lpppoint = ((left + 50, top - 50), (right + 50, top + 50), (left - 50, bottom - 50))

    while True:
        hdc = win32gui.GetDC(0)
        mhdc = win32gui.CreateCompatibleDC(hdc)
        hbit = win32gui.CreateCompatibleBitmap(hdc, sh, sw)
        win32gui.SelectObject(mhdc, hbit)

        win32gui.PlgBlt(
            hdc,
            lpppoint,
            hdc,
            left - 20,
            top - 20,
            (right - left) + 40,
            (bottom - top) + 40,
            None,
            0,
            0,
        )
        Sleep(150)


# Radial Blur Effect
def radial_blur_effect():
    HDC = GetDC(0)
    while True:
        for angle in range(0, 360, 10):
            temp_dc = CreateCompatibleDC(HDC)
            temp_bitmap = CreateCompatibleBitmap(HDC, sw, sh)
            SelectObject(temp_dc, temp_bitmap)
            BitBlt(temp_dc, 0, 0, sw, sh, HDC, 0, 0, SRCCOPY)
            BitBlt(HDC, 0, 0, sw, sh, temp_dc, 0, 0, sw, sh, SRCCOPY)
            DeleteObject(temp_bitmap)
            DeleteDC(temp_dc)
            Sleep(50)


# Bouncing Image Effect
def bouncing_image_effect():
    img_url = "https://yt3.googleusercontent.com/7vv6Q4rXEyM5o5E6dEhsCl5AdBiy2CLAFpsCPEonSYdK8YEpCh1Gah9dv2TgzUEBYV5T9bM3=s160-c-k-c0x00ffffff-no-rj"
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGBA")
    img = img.resize((200, 200), ANTIALIAS)

    HDC = GetDC(0)
    img_x, img_y = sw // 2, sh // 2
    dx, dy = 1, 1
    start_time = time.time()

    while True:
        temp_dc = CreateCompatibleDC(HDC)
        temp_bitmap = Image.frombuffer('RGBA', img.size, img.tobytes(), 'raw', 'RGBA', 0, 1)
        SelectObject(temp_dc, temp_bitmap)
        BitBlt(HDC, img_x, img_y, 200, 200, temp_dc, 0, 0, SRCCOPY)
        img_x += dx
        img_y += dy
        if img_x <= 0 or img_x + 200 >= sw:
            dx = -dx
        if img_y <= 0 or img_y + 200 >= sh:
            dy = -dy
        Sleep(50)
        if time.time() - start_time > 30:  # Run for 30 seconds
            break


# Black Square Effect
def black_square_effect():
    HDC = GetDC(0)
    black_square = Image.new("RGB", (100, 100), color="black")
    square = black_square.resize((sw, sh), ANTIALIAS)
    square.show()
    Sleep(120000)  # Wait 2 minutes after melting screen effect starts
    while True:
        square.show()
        Sleep(100)


# Start all effects
def start_effects():
    # Start melting screen effect
    melting_process = multiprocessing.Process(target=melting_screen_effect)
    melting_process.start()

    # Wait 2 minutes before starting black square effect
    Sleep(120000)

    # Start black square effect
    black_square_process = multiprocessing.Process(target=black_square_effect)
    black_square_process.start()

    # Start radial blur and rounded tunnel
    radial_blur_process = multiprocessing.Process(target=radial_blur_effect)
    rounded_tunnel_process = multiprocessing.Process(target=rounded_tunnel_effect)

    radial_blur_process.start()
    rounded_tunnel_process.start()

    # Wait for 30 seconds before starting the bouncing image effect
    Sleep(30000)
    bouncing_image_process = multiprocessing.Process(target=bouncing_image_effect)
    bouncing_image_process.start()

    # Join all processes
    melting_process.join()
    black_square_process.join()
    radial_blur_process.join()
    rounded_tunnel_process.join()
    bouncing_image_process.join()


if __name__ == "__main__":
    start_effects()