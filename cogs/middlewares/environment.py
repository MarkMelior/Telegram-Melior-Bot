from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class EnvironmentMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]
    
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs
    
    async def pre_process(self, obj, data, *args):
        data.update(**self.kwargs)

    # async def on_process(self, msg: types.Message, data: dict):
    #     if msg.from_user.id != config.tg_bot.admin_ids:
    #         pass