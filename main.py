from pprint import pprint
import csv
import re

if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    # pprint(contacts_list)

    # TODO 1: выполните пункты 1-3 ДЗ
    new_contacts_list = [contacts_list.pop(0)]
    row = 0
    for contact in contacts_list:
        row += 1
        new_contacts_list += [[''] * 7]
        # Разобрать ФИО на поля
        names = re.findall('[а-я]+', contact[0], flags=re.I)
        col = 0
        for name in names:
            new_contacts_list[row][col] = name
            col += 1
        # Привести все телефоны к одному формату
        country_code = re.findall('^(\+7|8).', contact[5])[0]
        city_code = re.findall('\d', contact[5])[0]

    # TODO 2: сохраните получившиеся данные в другой файл
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(new_contacts_list)