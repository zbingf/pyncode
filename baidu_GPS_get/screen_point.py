import time,os
import pyautogui
import pyperclip


# ---------------------------------
# ---------------------------------
xs, ys = [], []
lines = ['地图-左上角', '地图-右下角', '坐标-复制按键', '粘贴位置']
for n in range(3):
	print(lines[n])
	a = input()
	
	# 获取屏幕的尺寸
	screenWidth, screenHeight = pyautogui.size()
	x, y = pyautogui.position()
	xs.append(x)
	ys.append(y)
	
	#返回鼠标的坐标
	print('屏幕尺寸: (%s %s),  鼠标坐标 : (%s, %s)' % (screenWidth, screenHeight, x, y))
	# 每个1s中打印一次 , 并执行清屏
	time.sleep(1)


# ---------------------------------
# ---------------------------------
results = []
x1, x2, x3 = xs
y1, y2, y3 = ys

pyautogui.click(x1, y1)
time.sleep(1)

dt = 1

# 左上点
# img_path = 'map_02.png'
pyautogui.click(x1, y1)
time.sleep(dt)
# pyautogui.click(x1, y1)
# time.sleep(0.3)
# im = pyautogui.screenshot()
# im.save(img_path) # 保存图片


pyautogui.click(x3, y3)
time.sleep(dt)
# pyautogui.click(x4, y4)
# time.sleep(0.3)
# pyautogui.hotkey('ctrl', 'v')
# pyautogui.typewrite(';')

results.append(pyperclip.paste())

# 右下点
# img_path = 'map_03.png'
pyautogui.click(x2, y2)
time.sleep(dt)
# pyautogui.click(x2, y2)
# time.sleep(0.3)
# im = pyautogui.screenshot()
# im.save(img_path) # 保存图片


pyautogui.click(x3, y3)
time.sleep(dt)
# pyautogui.click(x4, y4)
# time.sleep(0.3)
# pyautogui.hotkey('ctrl', 'v')


# pyautogui.hotkey('alt', 'a')
# pyautogui.hotkey('ctrl', 'c')

results.append(pyperclip.paste())


# with open('result.txt', 'w') as f:
# 	f.write('\n'.join(results))


# 截图
# img_path = 'map_01.png'
img_path = ';'.join(results)+'.png'
im = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
im.save(img_path) # 保存图片


print(results)
