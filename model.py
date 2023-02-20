import psycopg2

create_texts_table = """CREATE TABLE IF NOT EXISTS texts(
        id serial PRIMARY KEY,
        file_name text NOT NULL,
        line_data text DEFAULT NULL,
        str_len int NOT NULL,
        created_on date DEFAULT CURRENT_DATE); 
        """
DATABASE = 'flask_db'
PASSWORD = ''
HOST = 'localhost'
USER = 'postgres'
class FDataBase:
    def __init__(self):
        self.db = DATABASE
        self.connection = self.create_db_connection(self)
        self.cursor = self.connection.cursor()
        self.execute_query(create_texts_table)

    @staticmethod
    def create_db_connection(self, *args, **kwargs):
        connection = None

        try:
            # connect to exist database
            connection = psycopg2.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                port=6000
            )
            connection.autocommit = True
            print("MySQL Database connection successful")

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT version();"
                )
                print(f"Server version: {cursor.fetchone()}")
        except Exception as _ex:
            print(f'[INFO] Error {_ex} while working with PostgreSQL.')
        return connection

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Table query successful")
        except Exception as _ex:
            print(f'[INFO] Error {_ex} while working with PostgreSQL on query: {query}')

    def read_all_query(self, table):
        result = None
        try:
            self.cursor.execute(f'SELECT * FROM {table};')
            result = self.cursor.fetchall()
            return result
        except Exception as _ex:
            print(f'[INFO] Error {_ex} while working with PostgreSQL on table: {table}')

    def hundred_rows_query(self, table, amount):
        result = None
        try:
            self.cursor.execute(f'SELECT * FROM {table} ORDER BY str_len DESC LIMIT {amount};')
            result = self.cursor.fetchall()
            return result
        except Exception as _ex:
            print(f'[INFO] Error {_ex} while working with PostgreSQL on table: {table}')

    def insert_file_query(self, file_name: str, lines: list):
        result = None
        try:

            for i in range(len(lines)):
                str = "INSERT INTO texts (file_name, line_data, str_len) VALUES ('{file_name}', '{text}', {len});".format(
                    file_name=file_name, text=lines[i][1].replace("'", ','), len=lines[i][0])
                self.cursor.execute(str)
            return result
        except Exception as _ex:
            print(f'[INFO] Error {_ex} while working with PostgreSQL on table texts')
