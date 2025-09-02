from sqlalchemy import create_engine, text


class MainSQL:

    def __init__(self):
        self.engine = create_engine("postgresql://merionpg:UZObS42{8>}>@51.250.26.13/pg-x-clients-be", echo=True)

    def get_count_company(self, active: bool = None):
        with self.engine.connect() as connection:
            if active is None:
                query = text("SELECT * FROM company where deleted_at is :active")
            elif active:
                query = text("SELECT * FROM company where deleted_at is null and is_active = :active")
            elif not active:
                query = text("SELECT * FROM company where deleted_at is null and is_active = :active")
            result = connection.execute(query, parameters={'active': active})
            data = result.fetchall()
            return len(data)


    def update_is_active(self, id: int, value: bool):
        with self.engine.connect() as connection:
            query = text("UPDATE company SET is_active = :value where id = :id")
            result = connection.execute(query, parameters={"id" : id, "value" : value})
            connection.commit()
