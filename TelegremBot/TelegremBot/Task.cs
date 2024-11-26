using System;
namespace TelegramBot
{
    class Task // Готов, по мере послупления проблем можно будет изменить 
    {
        private string _name;
        private string _description;
        private int _priority;
        private DateOnly _startDate;
        private DateOnly _finishDate;
        public string Name { get => _name; set => _name = value; }
        public string Description { get => _description; set => _description = value; }
        public int Priority { get => _priority; set => _priority = value; }
        public DateOnly StartDate { get => _startDate; set => _startDate = value; }
        public DateOnly FinishDate { get => _finishDate; set => _finishDate = value; }

        public Task(string name, string description, DateOnly startDate, DateOnly finishDate, int priority = 1)
        {
            Name = name;
            Description = description;
            Priority = priority;
            StartDate = startDate;
            FinishDate = finishDate;
        }
    }
}
