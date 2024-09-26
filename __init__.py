from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot,  MessageEvent
from nonebot.adapters import Bot, Event

from . import SparkApi



from typing import Tuple
from nonebot.plugin import PluginMetadata
from zhenxun.configs.config import Config
from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.withdraw_manage import WithdrawManager

# SparkApi 配置
appid = "XXXXXXXXXXXXXXXXX"
api_secret = "XXXXXXXXXXXXXXXXX"
api_key = "XXXXXXXXXXXXXXXXX"
domain = "generalv2"
Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"


__zx_plugin_name__ = "星火"
__plugin_usage__ = """
usage：
    星火AI
    指令：
       星火 
""".strip()
__plugin_des__ = "星火AI"
__plugin_cmd__ = ["星火"]
__plugin_version__ = 0.1
__plugin_author__ = 'Shouzi'
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["星火AI"],
}


__plugin_meta__ = PluginMetadata(
    name="星火AI",
    description="使用 星火AI 的 Nonebot 插件",
    usage="""
    星火 你的问题
    示例: 星火 你的问题
    """.strip(),
    extra=PluginExtraData(
        author="shouzi",
        version="0.1",
        configs=[
            RegisterConfig(
                key="WITHDRAW_Spark_AI_MESSAGE",
                value=(0, 1),
                help="自动撤回，参1：延迟撤回Spark_AI时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
                default_value=(0, 1),
                type=Tuple[int, int],
            ),
        ],
    ).dict(),
)

xinghuo = on_message(priority=100)
@xinghuo.handle()
async def _(bot: Bot, event: Event):
    if not isinstance(event, MessageEvent):
        return

    user_input = str(event.message) 
    if not user_input:
        return

    if not user_input.startswith('星火 '):
        return

    user_input = user_input[3:].strip() 

    if not user_input:
        return

    question = checklen(getText("user", user_input))
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)

    answer = SparkApi.answer
    question.clear()
    await xinghuo.finish(answer)




text = []

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
