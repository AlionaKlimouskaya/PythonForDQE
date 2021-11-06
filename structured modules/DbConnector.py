import sqlite3


class DbConnector:
    def __init__(self, database_url):
        self.database_url = database_url
        self.connection = sqlite3.connect(self.database_url)
        self.cursor = self.connection.cursor()

    def is_table_exists(self, table_name):
        query = f"SELECT count(1) FROM pragma_table_info('{table_name}');"
        self.cursor.execute(query)
        return int(self.cursor.fetchone()[0]) > 0

    def create_table(self, table_name, table_parameters):
        parameters = ',\n'.join([f'{key} {value}' for key, value in table_parameters.items()])
        query = f"""CREATE TABLE {table_name}
        (msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
        {parameters});"""
        self.cursor.execute(query)
        print(f'Table {table_name} was created.')

    def insert_row(self, table_name, datadict):
        columns = [key for key in datadict.keys()]
        values = [f"'{datadict[col]}'" for col in columns]
        query = f"INSERT INTO {table_name}({', '.join(columns)}) values ({', '.join(values)});"
        self.cursor.execute(query)
        self.connection.commit()

    def is_duplicate(self, table_name, datadict):
        params = ' AND '.join([f"{key} = '{datadict[key]}'" for key in datadict.keys() if 'PublishDate' not in key])
        query = f"SELECT COUNT(*) FROM {table_name} WHERE {params};"
        self.cursor.execute(query)
        return int(self.cursor.fetchone()[0]) > 0

    def ddl_schema_table(self, table_name, table_parameters):
        check_table = self.is_table_exists(table_name)
        if not check_table:
            self.create_table(table_name, table_parameters)

    def process(self, table_name, table_parameters, datadict):
        self.ddl_schema_table(table_name, table_parameters)
        if not self.is_duplicate(table_name, datadict):
            self.insert_row(table_name, datadict)
            print(f'Row was inserted into table {table_name} in database.')
        else:
            print(f'DUPLICATE. Row was NOT INSERTED into database table {table_name}.')
