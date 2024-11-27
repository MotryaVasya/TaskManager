using Telegram.Bot.Types;
using TelegremBot;

namespace TelegramBot
{
    class TaskManager
    {
        private static List<Task> _tasks;
        public static List<Task> Tasks { get => _tasks; set => _tasks = value; }
        public TaskManager(List<Task> tasks)
        {
            Tasks = tasks;
        }
        public static string AddTask(Task task)// по возможности улучшить 
        {
            if (Exist(task))
            {
                Tasks.Add(task);
                return MessageInfo.GetMessage(TypeMessage.TaskAdded);
            }
            return MessageInfo.GetMessage(TypeMessage.Nonexistent);

        }
        public static string RemoveTask(Task task) // по возможности улучшить  
        {
            if (Exist(task))
            {
                Tasks.Remove(task);
                return MessageInfo.GetMessage(TypeMessage.TaskDeleted);
            }
            return MessageInfo.GetMessage(TypeMessage.Nonexistent);
        }
        public static string UpdateTask(Task task) // доделать UpdateTask
        {
            if (Exist(task))
            {
                foreach (var item in Tasks)
                {
                    if (item == task)
                    {
                        item.Name = task.Name;
                        item.Description = task.Description;
                        item.StartDate = task.StartDate;
                        item.FinishDate = task.FinishDate;
                        item.Priority = task.Priority;
                        break;
                    }

                }
                return MessageInfo.GetMessage(TypeMessage.TaskUpdated);
            }
            return MessageInfo.GetMessage(TypeMessage.Nonexistent);
        }
        private static bool Exist(Task task) // может переделать 
        {
            return Tasks.Contains(task);
        }

    }
}
