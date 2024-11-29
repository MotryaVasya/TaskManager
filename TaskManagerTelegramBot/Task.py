from datetime import date
class Task:  # Готов, по мере поступления проблем можно будет изменить
    def __init__(self, name, description, start_date, finish_date, priority=1):
        self._name = name
        self._description = description
        self._priority = priority
        self._start_date = start_date
        self._finish_date = finish_date

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def finish_date(self):
        return self._finish_date

    @finish_date.setter
    def finish_date(self, value):
        self._finish_date = value

