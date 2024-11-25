using Telegram.Bot.Types.ReplyMarkups;

namespace TelegramBot
{
    class Keyboard
    {
        public static ReplyKeyboardMarkup GetButtonKeyboard()
        {
            var kbrd = new ReplyKeyboardMarkup(new KeyboardButton[][]
            {
        new []  {
                new KeyboardButton("📋 Добавить задачу")
                },
        new[]
        {
            new KeyboardButton("🐈 Удалить задачу")
        },
        new[]
        {
            new KeyboardButton("💡 Изменить задачу")
        }
            });
            return kbrd;
        }
    }
}
