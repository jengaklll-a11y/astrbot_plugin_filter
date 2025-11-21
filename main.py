from astrbot.api.all import *

@register("astrbot_plugin_filter", "jengaklll-a11y", "关键词与用户过滤", "1.0.0")
class FilterPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        
        # --- 配置区域 ---
        # 在这里定义你要屏蔽的关键词列表
        self.banned_keywords = ["笨蛋", "测试屏蔽", "不要回复"]
        
        # 在这里定义你要屏蔽的用户 ID (字符串格式)
        # 提示：可以在后台日志或打印 event.get_sender_id() 查看用户ID
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
            # 这是一个被屏蔽的用户
            print(f"[FilterPlugin] 拦截黑名单用户: {sender_id}")
            
            # 停止事件传播！
            # 这意味着：大模型、后续的其他插件都将无法收到这条消息
            event.stop_event() 
            
            # 可选：回复一条提示（如果不希望回复，直接 return 即可）
            # await event.send("您已被管理员禁止使用此机器人。")
            return

        # 3. 检查消息是否包含违禁词
        for keyword in self.banned_keywords:
            if keyword in message_text:
                # 发现违禁词
                print(f"[FilterPlugin] 拦截违禁词: {keyword}")
                
                # 停止事件传播
                event.stop_event()
                
                # 可选：回复警告
                await event.send(f"检测到敏感词“{keyword}”，消息已拦截。")
                return
