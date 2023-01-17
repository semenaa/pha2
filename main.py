import csv
import re

if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    # pprint(contacts_list)

    # Набить второй список из "исправленных" строк
    new_contacts_list = [contacts_list[0]]
    row = 0
    for contact in contacts_list:
        new_contacts_list += [[''] * 7]
        # Разобрать ФИО на поля
        names = re.findall('[а-я]+', contact[0], flags=re.I)
        names += re.findall('[а-я]+', contact[1], flags=re.I)
        col = 0
        for name in names:
            new_contacts_list[row][col] = name
            col += 1

        # Привести все телефоны к одному формату
        phone = re.search('(\+7|8)\s*[(]?(\d{3})[)]?\s*-?(\d{3})-?(\d{2})-?(\d{2})\s*[(]?(доб\w*\.?)?\s*(\d*)[)]?',
                          contact[5])
        if phone is not None:
            new_contacts_list[row][5] = phone.group(1) + '(' + phone.group(2) + ')' + \
                phone.group(3) + '-' + phone.group(4) + '-' + phone.group(5)
            # добавочные номера
            if phone.group(6) is not None:
                new_contacts_list[row][5] += ' ' + phone.group(6) + phone.group(7)

        # Скопировать организацию и e-mail
        new_contacts_list[row][3] = contacts_list[row][3]
        new_contacts_list[row][4] = contacts_list[row][4]
        new_contacts_list[row][6] = contacts_list[row][6]
        row += 1
    new_contacts_list.pop(-1)

    def merge(contact, another_contact):
        counter = 0
        for col in contact:
            if col == '':
                contact[counter] = another_contact[counter]
            counter += 1


    # Слить дублирующиеся записи, отметить лишние
    for contact in new_contacts_list:
        for another_contact in new_contacts_list:
            if another_contact == contact:
                continue
            counter = 0
            if contact[0] == another_contact[0]:
                if contact[1] == another_contact[1] or another_contact[1] == '':
                    if contact[2] == another_contact[2] or another_contact[2] == '':
                        merge(contact, another_contact)
                        another_contact[0] = '_delete_'
            counter += 1
    # Удалить лишние записи
    for contact in new_contacts_list:
        if contact[0] == '_delete_':
            new_contacts_list.remove(contact)

    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(new_contacts_list)
