import json


def merge_json(old_json_file, new_json_file):
    # Загрузка старого и нового JSON файлов
    with open(old_json_file, 'r', encoding='utf-8') as old_f:
        old_data = json.load(old_f)
    with open(new_json_file, 'r', encoding='utf-8') as new_f:
        new_data = json.load(new_f)
    # Создание словаря с названиями товаров из старого JSON файла и их соответствующими id_card и id_rub
    old_titles = {item['title']: {'id_card': item.get('id_card', None), 'id_rub': item.get('id_rub', None)} for item in
                  old_data}
    # Обновление нового JSON файла
    megen_data = []
    for item in new_data:
        title = item['title']
        if title in old_titles:
            # Добавление id_card и id_rub из старого JSON файла в соответствующий товар нового JSON файла
            item['id_card'] = old_titles[title]['id_card']
            item['id_rub'] = old_titles[title]['id_rub']
            megen_data.append(item)
        # Сохранение обновленного JSON файла
        with open(new_json_file, 'w', encoding='utf-8') as new_f:
            json.dump(new_data, new_f, ensure_ascii=False, indent=4)  # Пример использования


merge_json('all_product.json', 'test.json')
