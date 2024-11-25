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
        public static void AddTask(Task task)
        {
            if (Tasks.Contains(task)) 
            { 

            }
            
        }
        public static void RemoveTask() 
        {

        }
        public static void UpdateTask()
        {

        }

    }
}
