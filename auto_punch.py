import json

from selenium import webdriver
import aiohttp
import asyncio
from datetime import *
import logging
import send_qq_to_me


def get_second_delta():
    now_datetime = datetime.now()
    now_date = now_datetime.date()
    eight_clock = time(8, 0, 0)
    res = datetime.combine(now_date + timedelta(days=1), eight_clock)

    return int(res.timestamp() - now_datetime.timestamp())


class AutoPuncher:
    URL = 'https://xmuxg.xmu.edu.cn/xmu/login?app=214'
    URL2 = 'https://xmuxg.xmu.edu.cn/app/214'

    def __init__(self, username: str, password: str, chromedrive_path: str):
        self.username = username
        self.password = password
        self.chromedrive_path = chromedrive_path

    async def punch(self):

        option = webdriver.ChromeOptions()
        # option.add_argument('headless') #不显示前端
        driver = webdriver.Chrome(chrome_options=option, executable_path=self.chromedrive_path)

        try:

            # 进入登录页面
            driver.get(self.URL)
            driver.find_elements_by_class_name("primary-btn")[2].click()
            await asyncio.sleep(2)

            # 模拟登录
            driver.find_element_by_id("username").clear()
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("username").send_keys(self.username)
            driver.find_element_by_id("password").send_keys(self.password)
            driver.find_element_by_class_name("auth_login_btn").click()

            # 模拟跳转
            await asyncio.sleep(2)
            # driver.switch_to.window(driver.window_handles[-1])
            driver.get(self.URL2)
            await asyncio.sleep(3)

            # 点击我的表单
            driver.find_elements_by_class_name("tab")[1].click()
            await asyncio.sleep(5)

            # 判断是否已经打卡
            text = driver.find_element_by_xpath("//div[@data-name='select_1582538939790']").text
            while ('Yes' not in text):
                # vue和传统下拉框不一样
                driver.find_element_by_css_selector("[data-name='select_1582538939790']").click()
                await asyncio.sleep(3)
                driver.find_element_by_css_selector("[title='是 Yes'][class='btn-block']").click()
                # 点击保存
                driver.find_element_by_class_name("form-save").click()
                await asyncio.sleep(3)
                # 点击弹出框确定
                driver.switch_to.alert.accept()
                await asyncio.sleep(3)
                text = driver.find_element_by_xpath("//div[@data-name='select_1582538939790']").text

            # Finally, the browser window is closed. You can also call quit method instead of close.
            # The quit will exit entire browser whereas close will close one tab, but if just one tab was open,
            # by default most browser will exit entirely.
            return True
        except Exception as e:
            logging.error("Exception!!!", exc_info=True)
            return False
        finally:
            driver.quit()

    async def run(self):
        while True:

            res = await self.punch()
            fail_cnt = 0
            while (not res) and fail_cnt <= 10:
                res = await self.punch()
                fail_cnt += 1

            if fail_cnt<=10:
                logging.info("Successfully Punched.")

                send_task = asyncio.create_task(send_qq_to_me.send_qq_to_me("打卡搞掂！"))  # maybe can add a switch in here
                logging.info("Successfully create send task")
            else:
                logging.info("Punch Failed.")

                send_task = asyncio.create_task(send_qq_to_me.send_qq_to_me("打卡失败太多次了，请手动检查log确认错误原因"))  # maybe can add a switch in here
                logging.info("Successfully create send task")

            # Wait until tomorrow
            time_to_sleep = get_second_delta()
            logging.info("Wait until tomorrow 8:00 am. Wait seconds: %s", time_to_sleep)
            await asyncio.sleep(time_to_sleep)
            await send_task


if __name__ == '__main__':

    logging.basicConfig(filename='./log.txt', format="%(levelname)s , %(asctime)s: %(message)s", level=logging.DEBUG)

    with open('./login.json', 'r', encoding='utf8') as f:
        j = json.load(f)

    logging.info("Json loaded.")

    autopuncher = AutoPuncher(
        j['username'],
        j['password'],
        j['chrome_path']
    )

    logging.info("Autopuncher Instantiated.")

    try:
        logging.info("Begin to run loop.")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(autopuncher.run())
    finally:
        logging.info("Stopped.")
        loop.close()
