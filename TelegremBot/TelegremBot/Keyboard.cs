using Telegram.Bot.Types.ReplyMarkups;
using TelegremBot;

namespace TelegramBot
{
    class Keyboard 
    {
        public static ReplyKeyboardMarkup GetButtonKeyboard()
        {
            var kbrd = new ReplyKeyboardMarkup(new KeyboardButton[][]
            {
        new []  {
                new KeyboardButton(MessageInfo.GetMessage(TypeMessage.TaskAdd))
                },
        new[]
        {
            new KeyboardButton(MessageInfo.GetMessage(TypeMessage.TaskDelete))
        },
        new[]
        {
            new KeyboardButton(MessageInfo.GetMessage(TypeMessage.TaskUpdate))
        },
        new []
        {
            new KeyboardButton(MessageInfo.GetMessage(TypeMessage.ShowTasks))
        },
        new []
        {
            new KeyboardButton(MessageInfo.GetMessage(TypeMessage.ModifyLanguage))
        }
            });
            return kbrd;
        }
    }
}
