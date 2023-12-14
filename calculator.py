from PIL import ImageGrab
import keyboard
from cnocr import CnOcr
import re
import time
import sys


def extract_number(string) -> int:
    numbers = re.findall(r"[+-]?\d+", string)
    if len(numbers) == 0:
        numbers = re.findall(r"\d+", string)
    return int(numbers[0])


def calc(money, origin_salary, price, item_salary, _round, guigui: bool):
    cur_salary = origin_salary
    bought_salary = origin_salary + item_salary
    cur_money = money
    bought_money = money - price
    for i in range(1, 21 - _round):
        cur_profit = cur_salary * 0.2
        bought_profit = bought_salary * 0.2
        if guigui:
            gc_salary = cur_salary * 4 // 5
            gb_salary = bought_salary * 4 // 5
            cur_money = cur_money + cur_money // 5 + gc_salary * 0.2
            bought_money = bought_money + bought_money // 5 + gb_salary * 0.2
        else:
            cur_money = cur_money + cur_profit
            bought_money = bought_money + bought_profit
        cur_salary = cur_salary + cur_salary // 20
        bought_salary = bought_salary + bought_salary // 20
    return round(bought_money - cur_money)


gap = 275
_round = 0
salary = 0
money = 0
ocr = CnOcr()
guigui = False
print("准备就绪")

while True:
    if keyboard.is_pressed("f2"):
        bbox_attack = []
        bbox_salary = [400, 715, 500, 745]
        bbox_round = [1633, 981, 1808, 1027]
        bbox_hero = [680, 200, 720, 225]
        bbox_hero_price = [665, 400, 720, 430]
        bbox_item = [585, 560, 745, 710]
        bbox_item_price = [665, 740, 720, 770]
        bbox_money = [1630, 24, 1700, 51]
        bbox_refresh = [1750, 340, 1795, 360]

        image = ImageGrab.grab()
        print("-----------------------------------------------------------")

        image_round = image.crop(box=bbox_round)
        output = ocr.ocr(image_round)[0]
        result = str(output["text"])
        _round = extract_number(result)
        print(f"第{_round}回合前商店")

        image_money = image.crop(box=bbox_money)
        output = ocr.ocr(image_money)[0]
        result = str(output["text"])
        if result == "O":
            result = "0"
        money = int(result)
        print(f"当前魂晶为：{money}")

        image_salary = image.crop(box=bbox_salary)
        output = ocr.ocr(image_salary)[0]
        result = str(output["text"])
        if result == "O":
            result = "0"
        salary = int(result)
        print(f"当前投资为：{salary}")

        if guigui:
            image_refresh = image.crop(box=bbox_refresh)
            output = ocr.ocr(image_refresh)[0]
            result = str(output["text"])
            if result == "O":
                result = "0"
            refresh = int(result)
            refresh_pro = calc(
                money=money,
                origin_salary=salary,
                price=refresh,
                item_salary=0,
                _round=_round,
                guigui=guigui,
            )
            print(f"刷新价格为：{refresh}，刷新将一共损失{-refresh_pro}魂晶")

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
                        money=money,
                        origin_salary=salary,
                        price=price,
                        item_salary=80,
                        _round=_round,
                        guigui=guigui,
                    )
                    pro270 = calc(
                        money=money,
                        origin_salary=salary,
                        price=price,
                        item_salary=270,
                        _round=_round,
                        guigui=guigui,
                    )
                    print(
                        f"检测到牧师，扣除价格{price}魂晶，80投资最终将带来{pro80}魂晶收益，270投资最终将带来{pro270}魂晶收益"
                    )
                elif guigui:
                    image_hero_price = image.crop(box=bbox_hero_price)
                    outd = ocr.ocr(image_hero_price)[0]
                    price = int(str(outd["text"]))
                    pro = calc(
                        money=money,
                        origin_salary=salary,
                        price=price,
                        item_salary=0,
                        _round=_round,
                        guigui=guigui,
                    )
                    print(f"购买第{i + 1}个英雄技能，一共将损失{-pro}魂晶（包括价格）")
            except Exception as e:
                print(f"第{i + 1}个英雄检测失败，错误信息：{e}")
            bbox_hero[0] = bbox_hero[0] + gap
            bbox_hero[2] = bbox_hero[2] + gap
            bbox_hero_price[0] = bbox_hero_price[0] + gap
            bbox_hero_price[2] = bbox_hero_price[2] + gap

        for i in range(0, 4):
            status = False
            try:
                image_item = image.crop(box=bbox_item)
                out = ocr.ocr(image_item)
                if guigui:
                    image_item_price = image.crop(box=bbox_item_price)
                    outd = ocr.ocr(image_item_price)[0]
                    price = int(str(outd["text"]))
                for output in out:
                    result = str(output["text"])
                    # print(f"{i+1}, {result}")
                    if "投资" in result:
                        i_salary = extract_number(result)
                        image_item_price = image.crop(box=bbox_item_price)
                        outd = ocr.ocr(image_item_price)[0]
                        price = int(str(outd["text"]))
                        pro = calc(
                            money=money,
                            origin_salary=salary,
                            price=price,
                            item_salary=i_salary,
                            _round=_round,
                            guigui=guigui,
                        )
                        print(f"检测到投资物品，扣除价格{price}魂晶，{i_salary}投资最终将带来{pro}魂晶收益")
                        status = True
                if guigui and not status:
                    pro = calc(
                        money=money,
                        origin_salary=salary,
                        price=price,
                        item_salary=0,
                        _round=_round,
                        guigui=guigui,
                    )
                    print(f"购买第{i + 1}个物品，一共将损失{-pro}魂晶（包括价格）")
            except Exception as e:
                print(f"第{i + 1}个物品检测失败，错误信息：{e}")
            bbox_item[0] = bbox_item[0] + gap
            bbox_item[2] = bbox_item[2] + gap
            bbox_item_price[0] = bbox_item_price[0] + gap
            bbox_item_price[2] = bbox_item_price[2] + gap
        print("-----------------------------------------------------------")
    if keyboard.is_pressed("f3"):
        print("程序正在退出")
        sys.exit()  # 轻度影响性能
        # break # 极度影响性能，原因未知
    if keyboard.is_pressed("f4"):
        guigui = not guigui
        print(f"是否为龟龟：{guigui}")
        time.sleep(0.1)
    time.sleep(0.01)
