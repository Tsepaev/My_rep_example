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


    def delete_company_by_id(self, id: int):
        with self.engine.connect() as connection:
            stmt = text("DELETE FROM company WHERE id = :id")
            result = connection.execute(stmt, parameters={"id" : id})
            connection.commit()

    def get_company_by_id(self, id: int):
        with self.engine.connect() as connection:
            stmt = text("SELECT id, name FROM company WHERE id = :id")
            result = connection.execute(stmt, parameters={"id" : id})
            data = result.fetchall()
            return data
