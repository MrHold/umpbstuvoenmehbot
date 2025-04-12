import time, datetime, re
import json
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
from src.db.sessions import get_db
from src.db.models.schedule import Schedule
from src.db.models.groups import Group
import asyncio

# def save_schedule_to_file():
#     base_url = 'https://voenmeh.ru/obrazovanie/timetables/'
#     groups = get_groups_local(base_url + "#1")  # Получаем группы
#     group_ids = list(groups.keys())  # ID всех групп

#     for i in range(1, 3125):
#         if i in group_ids:
#             group_ids.remove(i)  # Удаляем группы, которые уже есть в базе данных
#     schedule = get_schedule_local(base_url, group_ids)  # Парсим расписание

#     Сохраняем расписание в файл
#     with open("schedule_data.json", "w", encoding="utf-8") as f:
#         json.dump(schedule, f, ensure_ascii=False, indent=4)
#     print("Данные расписания сохранены в schedule_data.json")

# These functions are adapted from your scheduleparser/main.py draft.
# def get_groups_local(url):
#     driver = webdriver.Chrome()
#     driver.get(url)
#     time.sleep(10)  # wait for page load
#     response = driver.page_source
#     driver.quit()
#     soup = BeautifulSoup(response, 'html.parser')
#     group_select = soup.find('select', {'id': 'studsCbxGroupNumber'})
#     groups = {}
#     if group_select:
#         for option in group_select.find_all('option'):
#             groups[option['value']] = option.text
#     return groups

# def get_schedule_local(url, group_ids):
#     # returns a list with one schedule dump per group
#     driver = webdriver.Chrome()
#     driver.get(url + "#1")
#     time.sleep(6)  # wait for timetable JS
#     driver.execute_script("studs_ShowTimetable();")
#     schedules = {}
#     for group in group_ids:
#         # select the group
#         select_elem = driver.find_element("id", 'studsCbxGroupNumber')
#         select = Select(select_elem)
#         select.select_by_value(str(group))
#         driver.execute_script("studs_ShowTimetable();")
#         time.sleep(2)
#         response = driver.page_source
#         soup = BeautifulSoup(response, 'html.parser')
#         schedule_data = []
#         for table in soup.find_all('table', class_='timetable_table'):
#             day_header = table.find('tr', class_='timetable_table_day_row')
#             if not day_header:
#                 continue
#             day = day_header.get_text(strip=True)
#             entries = []
#             content_table = table.find('table', class_='timetable_table_content')
#             if content_table:
#                 rows = content_table.find_all('tr')[1:]
#                 for row in rows:
#                     cols = [col.get_text(strip=True) for col in row.find_all('td')]
#                     entries.append(cols)
#             schedule_data.append({'day': day, 'entries': entries})
#         schedules[group] = schedule_data
#     driver.quit()
#     return schedules

async def load_schedule_from_file():
    # Загружаем данные из файла
    with open("schedule_data.json", "r", encoding="utf-8") as f:
        schedule_data = json.load(f)

    async with get_db() as db:
        # Удаляем старые данные
        # await db.execute(Schedule)
        # await db.commit()

        # Вставляем новые данные
        for group_id, group_schedule in schedule_data.items():
            for day_item in group_schedule:
                day = day_item.get('day', '')
                for entry in day_item.get('entries', []):
                    if len(entry) < 4:
                        continue
                    time_field, subject, teacher, room = entry
                    teacher = teacher.rstrip(';')
                    room = str(room.rstrip(';'))
                    parts = time_field.split()
                    try:
                        start_time = datetime.datetime.strptime(parts[0], "%H:%M").time()
                        parity = parts[-1]
                    except Exception:
                        continue                    
                    group_id = int(group_id)
                    # if len(parity) > 15:
                    #     print(parity)
                    # if len(room) > 15:
                    #     print(room)
                    # if len(day) > 15:
                    #     print(day)
                    schedule_row = Schedule(
                        group_id=group_id,
                        parity=parity,
                        day_of_week=day,
                        start_time=start_time,
                        room=room,
                        subject=subject,
                        teacher=teacher
                    )
                    db.add(schedule_row)
        await db.commit()
    print("Данные расписания загружены в базу данных")


# async def update_schedules():
#     base_url = 'https://voenmeh.ru/obrazovanie/timetables/'
#     # Get groups (you can adjust which groups to update)
#     groups = get_groups_local(base_url + "#1")
#     group_ids = [int(gid) for gid in groups.keys()]
#     # Here you may narrow down the group_ids list if needed.
#     schedule_dict = get_schedule_local(base_url, group_ids)
    
#     async with get_db() as db:
#         # Delete all existing schedule rows
#         await db.execute("DELETE FROM schedules")
#         await db.commit()
    
#     # For each group, parse the schedule and insert rows.
#     for group in group_ids:
#         group_schedule = schedule_dict.get(group, [])
#         for day_item in group_schedule:
#             day = day_item.get('day', '')
#             for entry in day_item.get('entries', []):
#                 if len(entry) < 4:
#                     continue
#                 # entry example: ["10:50 Нечетная", "пр СОЦИОЛОГИЯ РИСО", "Сурина В.А.;", "530*;"]
#                 time_field, subject, teacher, _ = entry
#                 teacher = teacher.rstrip(';')
#                 # Extract the start time (ignore week type for now)
#                 parts = time_field.split()
#                 try:
#                     start_time = datetime.datetime.strptime(parts[0], "%H:%M").time()
#                 except Exception:
#                     continue
#                 # Set a default duration (e.g. 45 minutes)
#                 dt_start = datetime.datetime.combine(datetime.date.today(), start_time)
#                 dt_end = dt_start + datetime.timedelta(minutes=45)
#                 end_time = dt_end.time()
                
#                 schedule_row = Schedule(
#                     group_id=group,
#                     day_of_week=day,
#                     start_time=start_time,
#                     end_time=end_time,
#                     subject=subject,
#                     teacher=teacher
#                 )
#                 async with get_db() as db:
#                     db.add(schedule_row)
#                     await db.commit()
#     print("Расписание успешно обновлено.")

async def load_groups():
    # Загружаем данные из файла
    with open("groups.json", "r", encoding="utf-8") as f:
        groups_data = json.load(f)

    async with get_db() as db:
        # Удаляем старые данные
        # await db.execute("DELETE FROM groups")
        # await db.commit()

        # Вставляем новые данные
        for group_id, group_name in groups_data.items():
            group_row = Group(
                group_id=int(group_id),
                name=group_name
            )
            db.add(group_row)
        await db.commit()
    print("Данные групп загружены в базу данных")

if __name__ == "__main__":
    asyncio.run(load_schedule_from_file())
    # save_schedule_to_file()
    asyncio.run(load_groups())