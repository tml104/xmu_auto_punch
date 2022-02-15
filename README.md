# xmu_auto_punch

厦门大学自动打卡

配置好login.json并运行，然后他就会每天早上8点定时打卡。

基于python async（话是那么说，其实根本没用到什么async的特性……）

## 依赖

+ Python 3.6+：别太老就行
+ [Selenium](https://www.selenium.dev/)：一个Python的Webdriver库。使用`pip install selenium`安装。如果你的Python包管理使用的是conda那么应该已经自带了。
+ Google Chrome ：别太老就行
+ [Chrome Driver](https://sites.google.com/chromium.org/driver/) ：注意**版本要与你所使用的Chrome版本一致**。

## 使用

### 使用 Docker 部署

如果你使用Linux那么我推荐直接使用Docker来部署。

1. 使用git clone将本项目拉到本地：`git clone https://github.com/tml104/xmu_auto_punch.git`。
2. 参照下面 “在 Windows 下部署” 的第4步，新建login.json文件并修改选项。
3. 使用`docker build -t xmu_auto_punch:v3` 新建镜像（可能需要一些时间）。
4. 使用`docker run xmu_auto_punch:v3` 运行镜像。

### 在 Windows 下部署

（其实Windows下也能用Docker Desktop部署，不过会不会有什么问题就不得而知了）

1. 使用git clone将本项目拉到本地：`git clone https://github.com/tml104/xmu_auto_punch.git`。
2. 下载Chrome Driver，然后将其解压到一个目录下，然后取得chromedriver.exe的绝对路径（例如：`D:\\chromedriver_win32\\chromedriver.exe`，注意Windows下使用反下划线，填入json时应使用双反下划线，路径中不能有中文字符）
3. 安装依赖：`pip install -r requirements.txt`
4. 在当前目录下新建一个login.json并将如下模板复制进此文件中，然后将自己的学号、密码和chrome drive的路径替换掉（注意Windows下用的应该是双反下划线），其他设置的说明请参考下方：

```json
{
  "username": "学号",
  "password": "密码",
  "chrome_path": "/chromedriver",
  
  "send_qq_to_me": false,

  "send_email_to_me": true,
  "email_info":{
    "email_host":"smtp.qq.com",
    "port": 465,
    "email":"QQID@qq.com",
    "auth":"授权码（对于QQ邮箱来说是一个16字符的字符串）"
  }
}
```

- send_qq_to_me: （本人自用选项，如果你不想用的话请保持其为false）如果你使用cqhttp部署了qqbot并开启了http服务，那么将其设置为true可以令其发送信息到对应的qq号（硬编码在send_qq_to_me中）。
- send_email_to_me： 在打卡成功/失败时将信息发送到对应邮箱（使用smtp）。
- email_host, post：如果是用qq邮箱那么对应的端口就是上述默认值。可根据你使用的邮箱进行修改。
- email、auth：邮箱账号和授权码（注意不是密码）。以qq邮箱为例，授权码可去“qq邮箱>设置>账号>开启stmp服务”来获取。
  
5. 在当前目录运行: `python auto_punch.py`

## 参考项目

https://github.com/clancylian/punch_card