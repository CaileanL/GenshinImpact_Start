import pygetwindow
import os
import subprocess
import time
import cv2
import numpy as np
import pyautogui
import win32com.client
import win32con
import win32gui
from PIL import ImageGrab
import Play_mp3

# 检查原神是否已经启动
if os.system('tasklist /FI "IMAGENAME eq YuanShen.exe" 2>NUL | find /I /N "YuanShen.exe">NUL') == 0:
    print("原神 已在运行!")
    os.system('pause')
    exit()
# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False  # 关闭FailSafe

while True:
    # 截图
    screenshot = cv2.cvtColor(np.array(ImageGrab.grab(
        bbox=(0, 0, screen_width, screen_height))), cv2.COLOR_BGR2RGB)
    # 计算屏幕白色像素比例
    white_pixels = np.sum(
        np.all(screenshot >= np.array([250, 250, 250]), axis=2))  # 在二维进行操作，解决含原量>100%的问题
    total_pixels = screen_width * screen_height

    white_percentage = white_pixels / total_pixels * 100
    print(f"屏幕含原量{white_pixels} {total_pixels} {white_percentage}%")
    # 判断是否满足启动条件
    if white_percentage >= 90:
        break
# 获取快捷方式路径
shortcut = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\原神\原神.lnk'

# 解析快捷方式获取安装路径
shell = win32com.client.Dispatch("WScript.Shell")
install_dir = shell.CreateShortCut(shortcut)
install_dir = install_dir.TargetPath.replace('launcher.exe', '')

# 拼接游戏exe路径
game_exe = os.path.join(install_dir, 'Genshin Impact Game', 'YuanShen.exe')

# 创建过渡用的白色图片
transition_steps = 35
white_image = np.full((screen_height, screen_width, 3), 255, dtype=np.uint8)

# 创建过渡窗口并置顶
# 创建一个全屏窗口并命名为"Transition"
cv2.namedWindow('Transition', cv2.WND_PROP_FULLSCREEN)
# 设置窗口属性为全屏模式
cv2.setWindowProperty(
    'Transition', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 使用PyAutoGUI获取名为"Transition"的窗口对象
transition_window = pyautogui.getWindowsWithTitle("Transition")[0]

# 将鼠标移动到"Transition"窗口的左上角位置
pyautogui.moveTo(transition_window.left, transition_window.top)

# 在"Transition"窗口中展示截图
cv2.imshow('Transition', screenshot)

# 使用win32gui模块找到名为"Transition"的窗口句柄
hwnd = win32gui.FindWindow(None, "Transition")

# 获取"Transition"窗口的位置信息
CVRECT = cv2.getWindowImageRect("Transition")

# 使用win32gui模块设置窗口位置为最顶层，并设置窗口位置与大小
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0,
                      screen_width, screen_height, win32con.SWP_SHOWWINDOW)


# 原神，启动！
subprocess.Popen(game_exe)

# 进行过渡并在过渡窗口上显示
for step in range(transition_steps):
    alpha = (step + 1) / transition_steps
    blended_image = cv2.addWeighted(
        screenshot, 1 - alpha, white_image, alpha, 0)
    cv2.imshow('Transition', blended_image)
    cv2.waitKey(10)

# 找到所有最大化的窗口


def get_all_explorer_windows():
    def callback(hwnd, windows):
        window_text = win32gui.GetWindowText(hwnd)
        window_class = win32gui.GetClassName(hwnd)
        # print(window_class, window_text)
        if win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE) & win32con.WS_MAXIMIZE:
            windows.append((hwnd, window_text))
            # print("--------------added!")

    windows = []
    win32gui.EnumWindows(callback, windows)

    # 打印查找到的窗口标题和句柄
    for hwnd, window_text in windows:
        print(f"Window Handle: {hwnd}, Window Text: {window_text}")

    return windows


# 枚举窗口,找到名称包含"原神"的窗口
while True:
    # 获取目标窗口句柄
    hwnd2 = win32gui.FindWindow(None, "原神")
    if (hwnd2 != 0):
        print("捕获！")
        print(time.gmtime())

        for i in get_all_explorer_windows():
            win32gui.ShowWindow(i[0], win32con.SW_MINIMIZE)

        time.sleep(5)

        # 获取当前获得焦点的窗口句柄
        hwnd3 = win32gui.GetForegroundWindow()
        # 最小化那个窗口
        win32gui.ShowWindow(hwnd3, win32con.SW_MINIMIZE)

        # 关闭
        cv2.destroyWindow('Transition')
        # 设置窗口置顶
        # win32gui.MoveWindow(hwnd2, 0, 0, screen_width, screen_height, True)
        # win32gui.ShowWindow(hwnd2, win32con.SW_MAXIMIZE)
        # win32gui.SetWindowPos(hwnd2, win32con.HWND_TOPMOST, 0, 0,
        #                       screen_width, screen_height, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        # 播放音乐
        Play_mp3.play('./start.mp3')

        win = pygetwindow.getWindowsWithTitle("原神")[0]
        # win.hide()
        win.show()
        win.maximize()
        win.activate()

        print("原神启动！！！")
        print(time.gmtime())
        break

# time.sleep(1)
