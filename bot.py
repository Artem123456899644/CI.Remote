import asyncio
import json5
import sys
import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

version = "0.1"
commands = [
    {"name": "startBot", "send": "start"},
    {"name": "reloadBotInfo", "send": "reload"},
    {"name": "stopBot", "send": "stop"}
]

class MainBot:
    def __init__(self, infoBot, scriptBase):
        self.botInfo = infoBot
        self.scriptBase = scriptBase
        
        self.bot = None
        self.dispatcher = None
        self.router = None
        self.is_running = False

        
        
    async def startBot(self):
        self.bot = await self.connectToBot(self.botInfo)
        self.dispatcher = Dispatcher()
        self.router = Router()
        self.dispatcher.include_router(self.router)

        await self.menu.start()  # Здесь запускаем меню
        self.menu = TelegramMenu(self.bot, self.dispatcher, self.router, self.scriptBase)
        self.is_running = True
        await self.dispatcher.start_polling(self.bot)

    async def stopBot(self):
        if self.bot:
            await self.bot.close()
        if self.dispatcher:
            await self.dispatcher.storage.close()
        self.is_running = False

    def reloadBotInfo(self):
        if self.is_running:
            asyncio.create_task(self.stopBot())
            asyncio.create_task(self.startBot())

    @staticmethod
    def loadInfo(filename):
        absPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(absPath, 'r', encoding='utf-8') as file:
            info = json5.load(file)['mainBot']
            return {
                "key": info["key"],
                "user": {
                    "id": info["userID"],
                    "nick": info["userNick"]
                }
            }

    @staticmethod    
    def loadScriptsBase(filename):
        with open(filename, "r", encoding='utf-8') as file:
            base = json5.load(file)
            scriptBase = {}
            for k, v in base.items():
                commandsScripts = {i['name']: i['send'] for i in v['commands']}
                scriptBase[v['name']] = commandsScripts
            return scriptBase


    async def connectToBot(self, infoBot):
        try:
            botInstance = Bot(infoBot['key'])
            return botInstance
        except Exception as e:
            print(f"Error connecting to bot: {e}")
            return None

    async def sendMessage(self, message, infoBot):
        if self.bot:
            await self.bot.send_message(chat_id=infoBot['user']['id'], text=message)

    async def processCommand(self):
        loop = asyncio.get_event_loop()

        while True:
            command = await loop.run_in_executor(None, sys.stdin.readline)
            command = command.strip()

            if command:
                matched_command = next((item for item in commands if item['send'] == command), None)
                if matched_command:
                    if matched_command['send'] == 'start':
                        await self.startBot()
                    elif matched_command['send'] == 'reload':
                        self.reloadBotInfo()
                    elif matched_command['send'] == 'stop':
                        await self.stopBot()
                elif command.startswith("__send:"):
                    message = command[len("__send:"):].strip()  
                    await self.sendMessage(message, self.botInfo)

    async def run(self):
        await self.startBot()
        await self.processCommand()


class TelegramMenu:
    def __init__(self, bot: Bot, dp: Dispatcher, router: Router, script_base: dict):
        self.bot = bot
        self.dp = dp
        self.router = router
        self.script_base = script_base
        
        self.main_buttons = list(script_base.keys())
        self.selected_category = None  
        self.sub_buttons = {} 
        
        self.register_handlers()

    def generate_main_menu(self):
        """Создает главное меню кнопок"""
        keyboard = InlineKeyboardBuilder()
        for category in self.main_buttons:
            keyboard.button(text=category, callback_data=f"main_{category}")
        keyboard.adjust(2) 

        return keyboard.as_markup()

    def generate_sub_menu(self, category):
        self.selected_category = f"{category}_"
        self.sub_buttons = self.script_base[category] 

        keyboard = InlineKeyboardBuilder()
        for cmd_name, cmd_value in self.sub_buttons.items():
            keyboard.button(text=cmd_name, callback_data=f"sub_{cmd_name}")
        keyboard.adjust(2)

        return keyboard.as_markup()

    async def handle_main_button(self, callback: types.CallbackQuery):

        category = callback.data.split("_")[1] 
        markup = self.generate_sub_menu(category)

        await callback.message.edit_text(f"Выбрана категория: {category}\nВыберите команду:", reply_markup=markup)

    async def handle_sub_button(self, callback: types.CallbackQuery):
 
        command = callback.data.split("_")[1]
        self.selected_category += command  
        
        await callback.message.edit_text(f"Выполнена команда: {self.selected_category}")
        print(self.selected_category) 

    def register_handlers(self):

        @self.router.message(Command("start"))
        async def start_command(message: types.Message):
            await message.answer("Выберите категорию:", reply_markup=self.generate_main_menu())

        self.router.callback_query.filter(lambda c: c.data.startswith("main_"))(self.handle_main_button)
        self.router.callback_query.filter(lambda c: c.data.startswith("sub_"))(self.handle_sub_button)


if __name__ == '__main__':
    print("__log: Process Started")
    try:
        info = sys.stdin.read().strip()
        print("__log: Getted Info")
        mainInfo, scriptBaseInfo = info.split("\n")
        mainClass = MainBot(mainInfo, scriptBaseInfo)

        asyncio.run(mainClass.run())
    except Exception:
        print("__log: Нихуя не работает, иди исправляй гондон")
