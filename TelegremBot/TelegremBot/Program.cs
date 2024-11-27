using Telegram.Bot;
using Telegram.Bot.Types.ReplyMarkups;
using TelegremBot;
namespace TelegramBot
{
    class Program
    {

        static async System.Threading.Tasks.Task Main(string[] args) // доделать все кнопки, чтобы каждая имела свою функцию
        {

            BotManager.Go();
            Console.ReadLine(); // Чтобы приложение не завершалось
        }

    }

}
