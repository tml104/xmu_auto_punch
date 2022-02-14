# xmu_auto_punch

厦门大学自动打卡

配置好login.json，然后他就会每天早上8点定时打卡。

基于python async（话是那么说，其实根本没用到什么async的特性……）

## 依赖

+ Python 3.8：别太老就行
+ [Selenium](https://www.selenium.dev/)：一个Python的Webdriver库。使用`pip install selenium`安装。如果你的Python包管理使用的是conda那么应该已经自带了。
+ Google Chrome ：别太老就行
+ [Chrome Driver][https://sites.google.com/chromium.org/driver/] ：注意**版本要与你所使用的Chrome版本一致**。

## 使用

### 使用 Docker 部署

如果你使用Linux那么我推荐直接使用Docker来部署。

（待补充）

### 在 Windows 下部署

（其实Windows下也能用Docker Desktop部署，不过会不会有什么问题就不得而知了）

1. 使用git clone将本项目拉到本地：`git clone git@github.com:tml104/nowcoder_browser.git`。
2. 下载Chrome Driver，然后将其解压到一个目录下，然后取得chromedriver.exe的绝对路径（例如：`D:\chromedriver_win32\chromedriver.exe`）。注意路径中不能有中文字符。
3. 安装依赖：`pip install -r requirements.txt`
4. 在当前目录下新建一个login.json并将如下模板复制进此文件中，然后将自己的学号、密码和chrome drive的路径替换掉（注意Windows下用的应该是双反下划线）：
    ```json
        {
        "username": "学号",
        "password": "密码",
        "chrome_path": "D:\\chromedriver_win32\\chromedriver.exe"
        }
    ```
5. 在当前目录运行: `python auto_punch.py`