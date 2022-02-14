import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import aiohttp
import asyncio
from datetime import *
# import logging
from loguru import logger
import send_qq_to_me


def get_second_delta(h:int = 8, m:int = 0, s:int = 0):
    '''
        取得当前时间和早上8点的unix时间戳差
    '''
    now_datetime = datetime.now()
    now_date = now_datetime.date()
    eight_clock = time(h, m, s)

    if datetime.combine(now_date, eight_clock) - now_datetime >= timedelta(0):
        res = datetime.combine(now_date , eight_clock)
    else:
        res = datetime.combine(now_date + timedelta(days=1), eight_clock)

    return int(res.timestamp() - now_datetime.timestamp())


class AutoPuncher:
    URL = 'https://xmuxg.xmu.edu.cn/xmu/login?app=214'
    URL2 = 'https://xmuxg.xmu.edu.cn/app/214'

    def __init__(self, username: str, password: str, chromedrive_path: str):
        '''
            初始化
        '''
        self.username = username
        self.password = password
        self.chromedrive_path = chromedrive_path

    async def punch(self):
        '''
            尝试打卡
        '''

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=self.chromedrive_path)

        try:

            # 进入登录页面
            driver.get(self.URL)
            driver.find_elements_by_class_name("primary-btn")[2].click()

            logger.success("Find login page.")
            await asyncio.sleep(2)

            # 模拟登录
            driver.find_element_by_id("username").clear()
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("username").send_keys(self.username)
            driver.find_element_by_id("password").send_keys(self.password)
            driver.find_element_by_class_name("auth_login_btn").click()

            logger.success("Emulate login.")
            await asyncio.sleep(2)

            # 模拟跳转
            # driver.switch_to.window(driver.window_handles[-1])
            driver.get(self.URL2)

            logger.success("Jump.")
            await asyncio.sleep(2)

            # 点击我的表单
            driver.find_elements_by_class_name("tab")[1].click()

            logger.success("Click my table.")
            await asyncio.sleep(3)

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

            logger.exception("Exception occurred when punching.")
            return False

        finally:
            driver.quit()

    async def run(self):
        '''
            持久运行
        '''
        while True:

            res = await self.punch()
            fail_cnt = 0
            FAIL_CNT_UPB = 1
            while (not res) and (fail_cnt <= FAIL_CNT_UPB):
                res = await self.punch()
                fail_cnt += 1

            if fail_cnt<=FAIL_CNT_UPB:
                logger.success("Successfully Punched.")

                # send_task = asyncio.create_task(send_qq_to_me.send_qq_to_me("打卡搞掂！"))  # maybe can add a switch in here
                await send_qq_to_me.send_qq_to_me("打卡搞掂！")
                logger.info("Successfully create send task")

            else:
                logger.error("Punch Failed.")

                # send_task = asyncio.create_task(send_qq_to_me.send_qq_to_me("打卡失败太多次了，请手动检查log确认错误原因"))  # maybe can add a switch in here
                await send_qq_to_me.send_qq_to_me("打卡失败太多次了，请手动检查log确认错误原因")

                logger.info("Successfully create send task")

            # Wait until tomorrow
            time_to_sleep = get_second_delta()
            logger.info("Wait until tomorrow 8:00 am. Wait seconds: {deltatime_value}", deltatime_value = time_to_sleep)
            await asyncio.sleep(time_to_sleep)


if __name__ == '__main__':

    #logging.basicConfig(filename='./log.txt', format="%(levelname)s , %(asctime)s: %(message)s", level=logging.DEBUG)
    logger.add("file_{time}.log", rotation="1 month", backtrace=True, diagnose=True)

    # Load config
    with open('./login.json', 'r', encoding='utf8') as f:
        j = json.load(f)

    logger.info("Json config loaded.")

    # Init auto puncher
    autopuncher = AutoPuncher(
        j['username'],
        j['password'],
        j['chrome_path']
    )

    logger.info("Autopuncher Instantiated.")

    try:
        logger.info("Begin to run loop.")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(autopuncher.run())
    finally:
        logger.info("Stopped.")
        loop.close()
