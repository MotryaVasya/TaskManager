using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TelegremBot
{
    static class MessageInfo // заполнить поля RusMessage и EnMessage
    {
        public static int Num = 0;
        private static Dictionary<TypeMessage, string> RusMessage = new Dictionary<TypeMessage, string>()
        {
            { TypeMessage.WriteTextFound ,"Не правильный ввод данных,попробуйте ввести данные еще раз!" },
            { TypeMessage.TaskExist,"Такая задача уже существует" },
            { TypeMessage.NeedLetters,"Введите буквы!" },
#region TextForActionWithTask
            { TypeMessage.TaskAdded,"Задача добавлена!" },
            { TypeMessage.TaskDeleted,"Задача удалена!" },
            { TypeMessage.Nonexistent, "Такой задачи не существует!" },
            { TypeMessage.TaskUpdated, "Задача обновлена!" },
#endregion

#region TextForButtons
            { TypeMessage.ShowTasks, "Показать все задачи!" },
            { TypeMessage.TaskUpdate, "Обновить задачу!" },
            { TypeMessage.TaskDelete,"Удалить задачу!" },
            { TypeMessage.TaskAdd, "Добавить задачу!" },
            { TypeMessage.ModifyLanguage, "Изменить на Английский" }
#endregion
        };

        private static Dictionary<TypeMessage, string> EnMessage = new Dictionary<TypeMessage, string>()
        {
            { TypeMessage.WriteTextFound ,"Incorrect data entry, try entering the data again!" },
            { TypeMessage.TaskExist,"That task exist!" },
            { TypeMessage.NeedLetters,"Enter letters!" },
#region TextForActionWithTask
            { TypeMessage.TaskAdded,"Task added!" },
            { TypeMessage.TaskDeleted,"Task deleted!" },
            { TypeMessage.Nonexistent, "That task Non Existent!" },
            { TypeMessage.TaskUpdated, "Task updated!" },
#endregion

#region TextForButtons
            { TypeMessage.ShowTasks, "Show all tasks" },
            { TypeMessage.TaskUpdate, "Update task" },
            { TypeMessage.TaskDelete,"Delete task" },
            { TypeMessage.TaskAdd, "Add task" },
            { TypeMessage.ModifyLanguage, "Modify to Russian" }
#endregion
        };


        /// <summary>
        /// Возвращает нужный словарь с переводом по индексации
        /// </summary>
        /// <returns>Словарь с переводом</returns>
        private static Dictionary<TypeMessage, string> GetDictionary()
        {
            return Num == 0 ? RusMessage : EnMessage;
        }
        public static string GetMessage(TypeMessage message)
        {
            foreach (var item in GetDictionary())
            {
                if (message == item.Key)
                {
                    return item.Value;
                }
            }
            return string.Empty;
        }

    }
    public enum TypeMessage
    {
        WriteTextFound = 1,
        TaskAdded,
        TaskDeleted,
        NeedLetters,
        TaskExist,
        Nonexistent,
        TaskUpdated,

        ShowTasks,
        TaskUpdate,
        TaskDelete,
        TaskAdd,
        ModifyLanguage,
    }

}
