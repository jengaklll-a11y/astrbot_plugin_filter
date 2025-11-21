# 显式导入 event_handler 和 AstrMessageEvent，确保不会报错
from astrbot.api.event import event_handler, AstrMessageEvent
from astrbot.api.all import * @register("astrbot_plugin_filter", "YourName", "关键词与用户过滤", "1.0.0")
class FilterPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        
        # --- 配置区域 ---
        self.banned_keywords = ["笨蛋", "测试屏蔽", "不要回复"]
        self.banned_users = ["751418355", "QQ_OR_WX_ID_HERE"]
        # ----------------

    # 监听所有消息事件
    @event_handler 
    async def handle_message(self, event: AstrMessageEvent):
        """
        当机器人收到消息时触发此函数
        """
        
        # 1. 获取发送者 ID 和 消息文本
        sender_id = event.get_sender_id()
        message_text = event.message_str

        # 2. 检查用户是否在黑名单中
        if sender_id in self.banned_users:
            print(f"[FilterPlugin] 拦截黑名单用户: {sender_id}")
            event.stop_event() 
            return

        # 3. 检查消息是否包含违禁词
        for keyword in self.banned_keywords:
            if keyword in message_text:
                print(f"[FilterPlugin] 拦截违禁词: {keyword}")
                event.stop_event()
                await event.send(f"检测到敏感词“{keyword}”，消息已拦截。")
                return
