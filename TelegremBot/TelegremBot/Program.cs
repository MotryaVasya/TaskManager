using Telegram.Bot;
using Telegram.Bot.Types.ReplyMarkups;
namespace TelegramBot
{
    class Program
    {
        private static readonly string BotToken = "7559173892:AAGF9i5R8FiGhdM6M4UpjycTWDa8ku2Fyc8";

        static async System.Threading.Tasks.Task Main(string[] args) // сделать методы под все кнопки
        {
            var botClient = new TelegramBotClient(BotToken);

            Console.WriteLine("Бот запущен. Ожидаем сообщения...");
            botClient.StartReceiving(
                updateHandler: async (client, update, cancellationToken) =>
                {
                    if (update.Message?.Text?.ToLower() == "задача")
                    {
                        await client.SendTextMessageAsync(update.Message.Chat.Id, "Хорошо", cancellationToken: cancellationToken, replyMarkup: Keyboard. GetButtonKeyboard());
                    }
                    else
                    {
                        await client.SendTextMessageAsync(update.Message.Chat.Id, "Не правильный ввод данных", cancellationToken: cancellationToken);
                    }
                },
                errorHandler: (client, exception, cancellationToken) =>
                {
                    Console.WriteLine($"Ошибка: {exception.Message}");
                    return System.Threading.Tasks.Task.CompletedTask;
                }
            );

            Console.ReadLine(); // Чтобы приложение не завершалось
        }
    }

}
