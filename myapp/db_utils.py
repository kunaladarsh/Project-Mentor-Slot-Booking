import mysql.connector
from mysql.connector import pooling
from django.conf import settings

class DatabaseManager:
    _instance = None
    _pool = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._pool is None:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "adarshkunal",
                "database": "MentorSlotBooking",
                "auth_plugin": 'mysql_native_password',
                "pool_name": "mypool",
                "pool_size": 5
            }
            self._pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)

    def get_connection(self):
        return self._pool.get_connection()

    def execute_query(self, query, params=None, fetch=False):
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                return result
            
            connection.commit()
            return True
            
        except mysql.connector.Error as err:
            if connection:
                connection.rollback()
            raise err
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def execute_many(self, query, params_list):
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.executemany(query, params_list)
            connection.commit()
            return True
            
        except mysql.connector.Error as err:
            if connection:
                connection.rollback()
            raise err
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close() 