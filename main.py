from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, ConversationHandler
import os
import json
from enum import Enum
from user import UserLoginMethod, User

load_dotenv()

# Conversation states
CHOOSING_LOGIN, WAITING_JSON, SHOWING_FEATURES = range(3)

users = []

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(token).build()
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                CHOOSING_LOGIN: [CallbackQueryHandler(self.login_method_selected)],
                WAITING_JSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_json)],
                SHOWING_FEATURES: [CallbackQueryHandler(self.handle_feature_selection)]
            },
            fallbacks=[CommandHandler("start", self.start)]
        )
        
        self.application.add_handler(conv_handler)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        keyboard = [
            [InlineKeyboardButton("Google", callback_data="GOOGLE")],
            [InlineKeyboardButton("Facebook", callback_data="FACEBOOK")],
            [InlineKeyboardButton("Huawei", callback_data="HUAWEI")],
            [InlineKeyboardButton("PlayStation", callback_data="PLAYSTATION")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Welcome! Please choose your login method:",
            reply_markup=reply_markup
        )
        return CHOOSING_LOGIN
    
    async def login_method_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        method = UserLoginMethod[query.data]
        context.user_data['login_type'] = method.value  # Store it in context
        
        auth_url = f"https://live.radiance.thatgamecompany.com/account/auth/oauth_signin?type={method.value}&token="
        
        await query.edit_message_text(
            f"Please open this link and send me the JSON response:\n\n{auth_url}"
        )
        
        return WAITING_JSON
    
    async def handle_json(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            data = json.loads(update.message.text)
            
            if 'id' not in data or 'alias' not in data or 'token' not in data:
                await update.message.reply_text("Invalid JSON format. Please make sure it contains 'id', 'alias', and 'token' fields.")
                return WAITING_JSON
            
            telegram_id = update.effective_user.id
            login_type = context.user_data.get('login_type')
            
            global users
            users = [u for u in users if u.telegram_id != telegram_id]
            
            new_user = User(telegram_id, login_type, data['id'], data['alias'], data['token'])
            await new_user.auth()

            users.append(new_user)
            
            keyboard = [[InlineKeyboardButton("Show Friends Info", callback_data="show_friends")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"Login successful! Welcome {data['alias']}.\n\nChoose a feature:",
                reply_markup=reply_markup
            )
            
            return SHOWING_FEATURES
        except json.JSONDecodeError:
            await update.message.reply_text("Invalid JSON format. Please send valid JSON.")
            return WAITING_JSON
        except Exception as e:
            print(e)
            await update.message.reply_text("Unknown error occured.")
            return WAITING_JSON
    
    async def handle_feature_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        if query.data == "show_friends":
            telegram_id = update.effective_user.id
            user = next((u for u in users if u.telegram_id == telegram_id), None)
            
            if user:
                info = await user.get_friends_info()
                await query.edit_message_text(info)
            else:
                await query.edit_message_text("User not found. Please /start again.")
        
        return SHOWING_FEATURES
    
    def run(self) -> None:
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TelegramBot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    bot.run()