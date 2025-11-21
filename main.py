# 1. 显式导入所需的组件，避免 'NameError'
from astrbot.api.event import event_handler, AstrMessageEvent
from astrbot.api.all import Context, Star, register

# 2. 注册插件
@register("astrbot_plugin_filter", "jengaklll-a11y", "关键词与用户过滤", "1.0.0")
class FilterPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        
        # --- 配置区域 ---
        # 屏蔽关键词
        self.banned_keywords = ["笨蛋", "测试屏蔽", "不要回复"]
        # 屏蔽用户ID
        self.banned_users = ["751418355", "QQ_OR_WX_ID_HERE"]
        # ----------------

    # 3. 事件监听器
    @event_handler
    async def handle_message(self, event: AstrMessageEvent):
        """
        当机器人收到消息时触发此函数
        """
        # 获取发送者 ID 和 消息文本
        sender_id = event.get_sender_id()
        message_text = event.message_str

        # 调试打印：查看是谁发了什么 (方便你在后台获取 sender_id)
        # print(f"收到消息 -> 用户: {sender_id}, 内容: {message_text}")

        # --- 检查黑名单用户 ---
        if sender_id in self.banned_users:
            print(f"[FilterPlugin] 拦截黑名单用户: {sender_id}")
            event.stop_event() # 停止传播
            return

        # --- 检查违禁词 ---
        for keyword in self.banned_keywords:
            if keyword in message_text:
                print(f"[FilterPlugin] 拦截违禁词: {keyword}")
                event.stop_event() # 停止传播
                
                # 发送提示 (可选)
                await event.send(f"消息包含敏感词“{keyword}”，已被拦截。")
                return
