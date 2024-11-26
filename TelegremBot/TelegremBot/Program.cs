using Telegram.Bot;
using Telegram.Bot.Types.ReplyMarkups;
using TelegremBot;
namespace TelegramBot
{
    class Program
    {
        private static readonly string BotToken = "7559173892:AAGF9i5R8FiGhdM6M4UpjycTWDa8ku2Fyc8";

        static async System.Threading.Tasks.Task Main(string[] args) // доделать все кнопки, чтобы каждая имела свою функцию
        {
            MessageInfo.Num = 1;
            var botClient = new TelegramBotClient(BotToken);

            Console.WriteLine("Бот запущен. Ожидаем сообщения...");
            botClient.StartReceiving(
                updateHandler: async (client, update, cancellationToken) =>
                {

                    var a = await client.SendTextMessageAsync(update.Message.Chat.Id, "", cancellationToken: cancellationToken, replyMarkup: Keyboard.GetButtonKeyboard());



                    // await client.SendTextMessageAsync(update.Message.Chat.Id, "Не правильный ввод данных", cancellationToken: cancellationToken);

                },
                errorHandler: (client, exception, cancellationToken) =>
                {
                    Console.WriteLine($"Ошибка: {exception.Message}");
                    return System.Threading.Tasks.Task.CompletedTask;
                }
            );
            Console.ReadLine(); // Чтобы приложение не завершалось
        }
        static string GetString(IReplyMarkup replyMarkup)
        {
            if (MessageInfo.Num == 1)
            {
                MessageInfo.Num = 0;
            }
            else
            {
                MessageInfo.Num = 1;
            }
            return "ghgh";
        }
    }

}
