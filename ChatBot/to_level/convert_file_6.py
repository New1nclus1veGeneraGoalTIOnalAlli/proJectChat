import json
import pandas as pan
import os

class Theme_Load:
    def __init__(self):
        self._Tfile=None
        
    
    # def set_sheet(self,sheet_index):
    #     self._Tsheet=sheet_index
    # def get_list(self):
    #     if self._Tfile is not None:
    #         try:
    #             # Загружаем файл Excel и получаем названия листов
    #             return pan.ExcelFile(self._Tfile).sheet_names
    #         except Exception as e:
    #             print(f"Ошибка при чтении файла: {e}")
    #             return []
    #     else:
    #         return -1
    def set_file(self,file_ex):
        self._Tfile=file_ex
    def get_FIO(self):
        
        file_read=self._Tfile
        
        df = pan.read_excel(file_read, sheet_name="Worksheet")  # Укажите имя листа, если нужно
        

        mask = ~df["Тема урока"].str.contains(r"^Урок №.*? Тема", regex=True)
        
        if mask.any():  # Проверяем, есть ли записи, которые не начинаются с "Урок №"

            data_to_save = {}

    # Проходим по всем записям, соответствующим маске
            for index in df[mask].index:
                fio = df.loc[index, "ФИО преподавателя"]
                theme = df.loc[index, "Тема урока"]
                subject = df.loc[index, "Предмет"]

                # Если преподаватель уже есть в словаре
                if fio not in data_to_save:
                    data_to_save[fio] = {}  # Создаем новый словарь для предметов

                # Если предмет уже есть у преподавателя, добавляем тему
                if subject in data_to_save[fio]:
                    data_to_save[fio][subject].append(theme)
                else:
                    # Если предмета нет, создаем новый список тем
                    data_to_save[fio][subject] = [theme]

                    # Сохранение в JSON файл
            json_file_path = 'data.json'
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)

            return json_file_path  # Возвращаем путь к JSON файлу
        else:
            return None


class loading_pair:
    def __init__(self):
        self._df_pair = None
        #self._Pfile=file_ex_pair
    def set_file(self,file_ex):
        self._df_pair=pan.read_excel(file_ex, sheet_name='Worksheet')
    def get_Button_group(self):
        qwe=self._df_pair['Группа'].unique()
        return qwe.tolist()

    def get_group(self,name_group):
        Ngroup=name_group
        mask = self._df_pair["Группа"].str.contains(Ngroup, regex=True)
            
        if mask.any():
            try:
                # print(f"Студенты в группе '{self._Ngroup}':")
                # print("-" * 40)
                # for index, row in self._df_pair[self._mask].iterrows():
                #     print(f"Студент: {row['FIO']}, Посещенные пары: {row['pairs in total']}")
                list=[]
                for index, row in self._df_pair[mask].iterrows():

                    list.append(f"Студент: {row['FIO']}, Посещенные пары: {row['pairs in total']}")
                
                return list
            except KeyError:
                return -1
            except Exception :
                return -2
        else:
            return None
    
    def get_max_pair(self):
        if self._mask.any():
            # Используем маску для фильтрации DataFrame и получения максимального значения
            return self._df_pair.loc[self._mask, "pairs in total"].max()
        else:
            return None  # Или любое другое значение, если маска не содержит True
    
    

# file_path = '/home/b1lly/Документы/for_works/project/Отчет по темам занятий.xls'  # Замените на путь к вашему файлу
# excel_handler = Theme_Load(file_path)
# sheet_names = excel_handler.get_list()

# if sheet_names != -1:
#     print("Список листов в Excel:")
#     for sheet in sheet_names:
#         print(sheet)
# else:
#     print("Файл не указан.")
