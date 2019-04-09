import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime
from vk_api.utils import get_random_id
import sqlite3
# -*- coding: utf-8 -*-

class vkbot:
    """
    Класс vkbot
    """
    def select(self):
        """
        Запрос select
        
        Возврат
        -------
        rows : array
            Возвращает массив с выборкой из БД.
        bool
            Возвращает False
        
        Ошибки
        ------
        sqlite3.Error
            Возникает если не может создать или подключиться к БД, или выполнить запрос.
        """
        try:
            conn = sqlite3.connect('bd/my.db')        
            c = conn.cursor()
            c.execute('''CREATE TABLE if not exists users (id int auto_increment primary key,id_user int, date datetime)''')
            c.execute("SELECT id_user,date  FROM users")
            rows = c.fetchall()
            c.close()
            conn.close()
            return rows
        except sqlite3.Error as err:
            print(err)
            return False
    def close(self,c,conn):
        """
        Закрывает соединение.
        
        Параметры
        ---------
        c : object
            Объект курсора.
        conn : object
            Объект connection .
        """
        c.close()
        conn.close()
        
    def insert(self,id_user,date):
        """
        Закрывает соединение.
        
        Параметры
        ---------
        id_user : int
            Id пользователя обратившегося к боту.
        date : datetime
            Время обращения пользователя.

        Возврат
        -------
        c : object
            Возвращает объект курсора.
        conn : object
            Возвращает объект connection.
        bool
            Возвращает False       
        bool
            Возвращает True
            
        Ошибки
        ------
        sqlite3.Error
            Возникает если не может создать или подключиться к БД, или выполнить запрос.
        """
        try:
            conn = sqlite3.connect('bd/my.db')        
            c = conn.cursor()
            c.execute("INSERT INTO users (id_user,date) VALUES (?,?)",(id_user,date,))
            return True,c, conn
        except sqlite3.Error as err:
            print(err)
            return False,c,conn
    def main(self):
        """
        Основная функция, которая вызывает все остальные.

        Ошибки
        ------
        vk_api.VkApiError
            Возникает если не существует метода или сообщение не было отправлено пользователю.
        vk_api.AuthError
            Возникает если произошла ошибка при авторизации.
        OSError
            Возникает если произошла сетевая ошибка.
        IOError
            Возникает если не существует файла конфигурации.
        """  
        config = {}
        try:
            exec(open("config.py").read(),config)
            vk = vk_api.VkApi(token =config['token'])
            longpoll = VkLongPoll(vk)
            vk = vk.get_api()
        except (vk_api.AuthError,OSError,IOError) as error_msg:
            print(error_msg)
            return
        row = self.select()
        if row==False:
            return
        for val in row:
            print('Обращался пользователь с id:',val[0], 'Время:',val[1])
        try:            
            while True:
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                        if event.text == 'Дата':
                            valid,c,conn = self.insert(event.user_id,datetime.now())
                            if valid==True:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    random_id=get_random_id(),
                                    message= datetime.now()
                                    )
                                conn.commit()
                                self.close(c,conn)
                                print('Обращался пользователь с id:',event.user_id, 'Время:',datetime.now())
                            else:
                                self.close(c,conn)
                                return
                    continue
        except (vk_api.VkApiError) as error_msg:
            print(error_msg)
            return

