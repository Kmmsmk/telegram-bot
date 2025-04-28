import logging
import datetime
from telegram import Bot
from telegram.ext import CommandHandler, Application
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from database import insert_stats, get_last_stats
from config import TOKEN

# 配置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 Bot
bot = Bot(TOKEN)

# 频道列表
channels = ['@channel1', '@channel2', '@channel3', '@channel4', '@channel5']  # 这里添加你的频道

# 获取频道基本信息
def get_channel_stats(channel):
    url = f'https://api.telegram.org/bot{TOKEN}/getChat?chat_id={channel}'
    response = requests.get(url)
    data = response.json()
    
    if data['ok']:
        chat_info = data['result']
        return chat_info['title'], chat_info['members_count']
    return None, None

# 获取每日新增订阅人数
def get_daily_new_subscribers(channel):
    last_stats = get_last_stats(channel)
    if last_stats:
        today = datetime.date.today()
        last_date = last_stats['date']
        if today > last_date:
            return get_channel_stats(channel)[1] - last_stats['members_count']
    return 0

# 记录每日统计数据
def record_daily_stats():
    today = datetime.date.today().strftime("%Y-%m-%d")
    for channel in channels:
        title, members_count = get_channel_stats(channel)
        if title and members_count is not None:
            daily_new_subscribers = get_daily_new_subscribers(channel)
            insert_stats(channel, today, members_count, daily_new_subscribers)

# 启动定时任务
def start_scheduled_task():
    scheduler = BackgroundScheduler()
    scheduler.add_job(record_daily_stats, 'interval', hours=24)  # 每24小时执行一次
    scheduler.start()

# 启动机器人并提供命令
async def daily_stats(update, context):
    today = datetime.date.today().strftime("%Y-%m-%d")
    stats_message = f"今日统计 ({today}):\n"
    
    for channel in channels:
        title, members_count = get_channel_stats(channel)
        if title and members_count is not None:
            daily_new_subscribers = get_daily_new_subscribers(channel)
            stats_message += f"{title}: {members_count} 订阅人数, {daily_new_subscribers} 新增订阅\n"
        else:
            stats_message += f"{channel}: 获取数据失败\n"
    
    await update.message.reply_text(stats_message)

def main():
    # 初始化数据库
    from database import init_db
    init_db()

    # 启动定时任务
    start_scheduled_task()

    # 启动 Telegram bot
    application = Application.builder().token(TOKEN).build()

    # 注册命令处理器
    application.add_handler(CommandHandler("daily_stats", daily_stats))

    # 启动机器人
    application.run_polling()

if __name__ == '__main__':
    main()

