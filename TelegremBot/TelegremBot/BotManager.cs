using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Telegram.Bot;
using Telegram.Bot.Types.ReplyMarkups;
using TelegramBot;

namespace TelegremBot
{
    static class BotManager // модифицировать
    {
        private static readonly string BotToken = "7559173892:AAGF9i5R8FiGhdM6M4UpjycTWDa8ku2Fyc8";

        public static void Go()
        {
            MessageInfo.Num = 1;
            var botClient = new TelegramBotClient(BotToken);

            Console.WriteLine("Бот запущен. Ожидаем сообщения...");
            botClient.StartReceiving(
                updateHandler: async (client, update, cancellationToken) =>
                {

                    string userMessage = update.Message.Text;

                    if (userMessage == MessageInfo.GetMessage(TypeMessage.TaskAdd))
                    {
                        // Действия при нажатии кнопки "TaskAdd"
                    }
                    else if (userMessage == MessageInfo.GetMessage(TypeMessage.TaskDelete))
                    {
                        // Действия при нажатии кнопки "TaskDelete"
                        await client.SendMessage(
                            chatId: update.Message.Chat.Id,
                            text: "Вы выбрали удалить задачу.",
                            cancellationToken: cancellationToken
                        );
                    }
                    else if (userMessage == MessageInfo.GetMessage(TypeMessage.TaskUpdate))
                    {
                        // Действия при нажатии кнопки "TaskUpdate"
                        await client.SendMessage(
                            chatId: update.Message.Chat.Id,
                            text: "Вы выбрали обновить задачу.",
                            cancellationToken: cancellationToken
                        );
                    }
                    else if (userMessage == MessageInfo.GetMessage(TypeMessage.ShowTasks))
                    {
                        // Действия при нажатии кнопки "ShowTasks"
                        await client.SendMessage(
                            chatId: update.Message.Chat.Id,
                            text: "Вы выбрали показать задачи.",
                            cancellationToken: cancellationToken
                        );
                    }
                    else if (userMessage == MessageInfo.GetMessage(TypeMessage.ModifyLanguage))
                    {
                        await client.SendMessage(
                            chatId: update.Message.Chat.Id,
                            text: LanguageModified(),
                            cancellationToken: cancellationToken,
                            replyMarkup: Keyboard.GetButtonKeyboard()
                        );
                    }


                    // await client.SendTextMessageAsync(update.Message.Chat.Id, "Не правильный ввод данных", cancellationToken: cancellationToken);

                },
                errorHandler: (client, exception, cancellationToken) =>
                {
                    Console.WriteLine($"Ошибка: {exception.Message}");
                    return System.Threading.Tasks.Task.CompletedTask;
                }
            );
        }
        private static string LanguageModified()
        {
            if (MessageInfo.Num == 1)
            {
                MessageInfo.Num = 0;
            }
            else
            {
                MessageInfo.Num = 1;
            }
            return MessageInfo.GetMessage(TypeMessage.LanguageModified);
        }
    }
}
