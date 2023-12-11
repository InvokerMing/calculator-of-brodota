from PIL import ImageGrab
import keyboard
from cnocr import CnOcr
import sys
import re


def extract_number(string) -> int:
    numbers = re.findall(r"\d+", string)
    return int(numbers[0])


def calc(x=1000, x_salary=0, price=0, salary=0, round=1, guigui=True):
    y = x - price
    y2 = x
    y3 = x - price
    y4 = x

    for i in range(1, 21 - round):
        x_profit = x_salary * 0.2
        profit = (salary + x_salary) * 0.2
        y = y + y // 5 + profit
        y2 = y2 + y2 // 5 + x_profit
        y4 += x_profit
        y3 += profit
        x_salary += x_salary // 20
        salary += salary // 20
    if guigui:
        return y - y2
    else:
        return y3 - y4


gap = 275
round = 0
salary = 0
money = 0
ocr = CnOcr()
guigui = True
print("准备就绪")

while True:
    if keyboard.is_pressed("f2"):
        image = ImageGrab.grab()
        bbox_salary = [400, 715, 500, 745]
        bbox_round = [1633, 981, 1808, 1027]
        bbox_hero = [680, 200, 720, 225]  # 270
        bbox_hero_price = [665, 400, 720, 430]
        bbox_item = [585, 560, 745, 710]
        bbox_item_price = [665, 740, 720, 770]
        bbox_money = [1630, 24, 1700, 51]

        image_round = image.crop(box=bbox_round)
        output = ocr.ocr(image_round)[0]
        result = str(output["text"])
        round = extract_number(result) - 1
        print(f"第{round}回合")

        image_money = image.crop(box=bbox_money)
        output = ocr.ocr(image_money)[0]
        result = str(output["text"])
        money = int(result)
        print(f"当前魂晶为：{money}")

        image_salary = image.crop(box=bbox_salary)
        output = ocr.ocr(image_salary)[0]
        result = str(output["text"])
        salary = int(result)
        print(f"当前投资为：{salary}")

        for i in range(0, 4):
            try:
                image_hero = image.crop(box=bbox_hero)
                output = ocr.ocr(image_hero)[0]
                result = str(output["text"])
                # print(f"{i+1}, {result}")
                if "牧师" in result:
                    image_hero_price = image.crop(box=bbox_hero_price)
                    output = ocr.ocr(image_hero_price)[0]
                    result = str(output["text"])
                    price = int(result)
                    pro80 = calc(
                        x=money,
                        x_salary=salary,
                        price=price,
                        salary=80,
                        round=round,
                        guigui=guigui,
                    )
                    pro270 = calc(
                        x=money,
                        x_salary=salary,
                        price=price,
                        salary=270,
                        round=round,
                        guigui=guigui,
                    )
                    print(f"检测到牧师，扣除价格，80投资最终将带来{pro80}收益，270投资最终将带来{pro270}收益")
            except:
                print(f"第{i+1}个英雄检测失败")
            bbox_hero[0] = bbox_hero[0] + gap
            bbox_hero[2] = bbox_hero[2] + gap
            bbox_hero_price[0] = bbox_hero_price[0] + gap
            bbox_hero_price[2] = bbox_hero_price[2] + gap

        for i in range(0, 4):
            try:
                image_item = image.crop(box=bbox_item)
                out = ocr.ocr(image_item)
                for output in out:
                    result = str(output["text"])
                    # print(f"{i+1}, {result}")
                    if "投资" in result:
                        i_salary = extract_number(result)
                        image_item_price = image.crop(box=bbox_item_price)
                        outd = ocr.ocr(image_item_price)[0]
                        price = int(str(outd["text"]))
                        pro = calc(
                            x=money,
                            x_salary=salary,
                            price=price,
                            salary=i_salary,
                            round=round,
                            guigui=guigui,
                        )
                        print(f"检测到投资物品，扣除价格，{i_salary}投资最终将带来{pro}收益")
            except:
                print(f"第{i+1}个物品检测失败")
            bbox_item[0] = bbox_item[0] + gap
            bbox_item[2] = bbox_item[2] + gap
            bbox_item_price[0] = bbox_item_price[0] + gap
            bbox_item_price[2] = bbox_item_price[2] + gap
        print("-----------------------------------------------------------")
    if keyboard.is_pressed("f3"):
        print("程序正在退出")
        sys.exit()
    if keyboard.is_pressed("f4"):
        guigui = not guigui
        print(f"是否为龟龟：{guigui}")
