from datetime import datetime, date
import json
import datafile

def parse_config(config):
    #Валидация
    module = globals().get(config, None)
    if not module:
        return {}
    
    #Импорт ключей
    config_values = {}
    for key, value in module.__dict__.items():
        if key.startswith('_'):
            continue
        if key.startswith('__'):
            continue
        config_values[key] = date.fromisoformat(value)

    #Сортировка
    config_sorted = dict(sorted(config_values.items(), key=lambda item: item[1], reverse = True))

    #Вывод на экран
    print("#Settings")
    for key, value in config_sorted.items():
       print(f'{key:<30}:   {str(value):<100}')

    return config_sorted

def get_current_date():
    #Получение и вывод на экран текущей даты
    today = date.today()
    print('#Today')
    print(today)
    return today

def get_youngest_employee_date(settings):
    #Получение возраста самого младшего сотрудника
    youngest_employee_date = next(iter(settings.items()))[1]
    print('#Youngest employee date')
    print(youngest_employee_date)
    return youngest_employee_date

def days_delta(first_date, second_date):
    #Получение разницы в датах в днях
    if first_date > second_date:
        delta = first_date - second_date
    else:
        delta = second_date - first_date
    return delta.days

def years_delta(first_date, second_date):
    #Вычисление разницы в датах в годах
    years = second_date.year - first_date.year
    if second_date.month < first_date.month or (second_date.month == first_date.month and second_date.day < first_date.day):
        years -= 1
    return years


if __name__ == '__main__':
    settings = parse_config('datafile')
    
    today = get_current_date()

    youngest_employee_date = get_youngest_employee_date(settings)

    json_data = []
    for key, value in settings.items():
        birthday_to_today_days = days_delta(today, value)
        age_when_youngest_birthday = years_delta(value, youngest_employee_date)

        item = {}
        item["employee_name"] = key
        item["birthday_to_today_days"] = birthday_to_today_days
        item["age_when_youngest_birthday"] = age_when_youngest_birthday
        json_data.append(item)

    print("#Result")
    print(json.dumps(json_data, indent=4, sort_keys=True))
    with open('result.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)
        outfile.close()