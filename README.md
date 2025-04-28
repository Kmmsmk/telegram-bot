Telegram Channel Statistics Bot
这是一个用于统计 Telegram 频道的日活跃人数和每日新增订阅者的 Python 脚本。它会自动收集多个频道的统计数据，并每日向你指定的 Telegram 频道发送一份报告。

功能特点
获取 Telegram 频道的总订阅人数。

计算每日新增的订阅人数。

每日自动向指定的 Telegram 频道发送汇总报告。

将每日数据存储在 MySQL 数据库中，最多保存一周的数据。

支持多个 Telegram 频道。

环境要求
Python 3.x

MySQL 数据库

Telegram Bot Token

项目结构
telegram-bot/
│
├── bot.py             # 主机器人代码
├── config.py          # 配置文件，包括 Token 和数据库信息
├── database.py        # 数据库相关功能
├── requirements.txt   # 项目依赖包
└── README.md          # 项目文档
