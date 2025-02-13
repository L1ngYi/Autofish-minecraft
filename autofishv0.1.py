import pyautogui
import time
from PIL import ImageGrab, ImageDraw

# 全局变量
FISHING_BOBBER_COLOR = (165,31,26)  # 鱼漂的颜色
FISHING_BOBBER_COLOR_2 = (135,20,20)
FISHING_BOBBER_COLOR_3 = (166,31,26)
FISHING_BOBBER_REGION = None  # 鱼漂检测区域
FINSHING_BOX_SIZE = 100  # 鱼漂检测区域的大小（宽度和高度）
Game_BOBBER_REGION = None
Draw_BOBBER_REGION = None
def find_game_window():
    global Game_BOBBER_REGION
    # 获取当前活动窗口
    active_window = pyautogui.getActiveWindow()
    if active_window:
        print(f"当前活动窗口: {active_window.title}")
        print(f"位置: {active_window.left}, {active_window.top}")
        print(f"大小: {active_window.width}x{active_window.height}")
        Game_BOBBER_REGION = (active_window.left,active_window.top,active_window.width,active_window.height)
def cast_fishing_rod():
    """抛出钓鱼竿"""
    pyautogui.rightClick()
    time.sleep(1)
def draw_red_box():
    """在屏幕上绘制红框以标识检测区域"""
    # 截取屏幕
    screenshot = ImageGrab.grab()
    draw = ImageDraw.Draw(screenshot)

    # 绘制红框
    x, y, width, height = Draw_BOBBER_REGION
    draw.rectangle((x, y, x + width, y + height), outline="red", width=2)

    # 显示红框
    screenshot.show()

def is_bobber_color(pixel):
    r, g, b = pixel
    # 定义鱼漂颜色的范围
    return (80 <= r <= 255) and (15 <= g <= 50) and (15 <= b <= 50)

def find_fishing_bobber():
    """在游戏区域内查找鱼漂"""
    global FISHING_BOBBER_REGION
    screenshot = pyautogui.screenshot(region=Game_BOBBER_REGION)
    for x in range(screenshot.width):
        for y in range(screenshot.height):
            if is_bobber_color(screenshot.getpixel((x, y))):
                print(f"找到鱼漂！位置：({x + Game_BOBBER_REGION[0]}, {y + Game_BOBBER_REGION[1]})")
                FISHING_BOBBER_REGION = (x + Game_BOBBER_REGION[0], y + Game_BOBBER_REGION[1], FINSHING_BOX_SIZE, FINSHING_BOX_SIZE)
                return True
    print("未发现鱼漂位置")
    return False


def query_get_fish():
    """检测鱼漂下沉"""
    # 截取检测区域
    #global FISHING_BOBBER_REGION
    count = 0
    while True:
        
        screenshot = pyautogui.screenshot(region=FISHING_BOBBER_REGION)
        for x in range(screenshot.width):
            for y in range(screenshot.height):
                if is_bobber_color(screenshot.getpixel((x, y))):
                    print(f"鱼漂没有下沉。位置：({x + FISHING_BOBBER_REGION[0]}, {y + FISHING_BOBBER_REGION[1]})")
                    return False
        count += 1
        
        if(count > 5):
            print("鱼漂已经下沉！")
            return True
        continue

def auto_fish():
    """自动钓鱼主循环"""
    while True:
        cast_fishing_rod()
        time.sleep(3)  # 等待鱼漂落水
        #找鱼漂的位置 定义鱼漂浮动检测框
        while not find_fishing_bobber():
            time.sleep(0.01)
        while not query_get_fish():
            time.sleep(0.1)
        print("上鱼！收杆！")
        reel_fishing_rod()
        time.sleep(1)

def reel_fishing_rod():
    """收竿"""
    pyautogui.rightClick()
    time.sleep(1)
if __name__ == "__main__":
    print("自动钓鱼脚本将在五秒后启动，请切换到游戏界面")
    time.sleep(5)
    find_game_window()
    # draw_red_box()
    print("自动钓鱼脚本启动")
    try:
        auto_fish()
    except KeyboardInterrupt:
        print("自动钓鱼脚本已停止。")
    #draw_red_box()  # 绘制红框

