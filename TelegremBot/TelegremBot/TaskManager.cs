using Telegram.Bot.Types;

namespace TelegramBot
{
    class TaskManager
    {
        private static List<Task> _tasks;
        private static string _message;
        public static List<Task> Tasks { get => _tasks; set => _tasks = value; }
        public static string Message { get => _message; set => _message = value; }
        public TaskManager(List<Task> tasks)
        {
            Tasks = tasks;
        }
        public static string AddTask(Task task)// по возможности улучшить 
        {
            Message = "Задача добавлена";
            if (Exist(task)) 
            {
                Message = "такая задача уже есть";
                return Message;
            }
            Tasks.Add(task);
            return Message;
            
        }
        public static string RemoveTask(Task task) // по возможности улучшить  
        {
            Message = "Задача удалена";
            if (Exist(task))
            {
                Tasks.Remove(task);
                return Message;
            }
            return Message;
        }
        public static string UpdateTask(Task task) // доделать UpdateTask
        {
            Message = "Задача обновлена";
            if (Exist(task))
            {
                foreach (var item in Tasks)
                {
                    if (item == task)
                    {

                    }
                    
                }
                return Message;
            }
            Message = "";
            return Message;
        }
        private static bool Exist(Task task) // может переделать 
        {
            return Tasks.Contains(task);
        }

    }
}
