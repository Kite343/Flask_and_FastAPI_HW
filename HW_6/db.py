import datetime
import databases
import sqlalchemy
from settings import settings

db = databases.Database(settings.DATABASE_URL)
mdt = sqlalchemy.MetaData()

users_db = sqlalchemy.Table("users", mdt,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("name", sqlalchemy.String(32)),
                            sqlalchemy.Column("surname", sqlalchemy.String(32)),
                            sqlalchemy.Column("email", sqlalchemy.String(128)),
                            sqlalchemy.Column("password", sqlalchemy.String(64)),
                            )


products_db = sqlalchemy.Table("products", mdt,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("name_product", sqlalchemy.String(128)),
                            sqlalchemy.Column("description", sqlalchemy.String(500)),
                            sqlalchemy.Column("price", sqlalchemy.FLOAT(128)),
                            )


orders_db = sqlalchemy.Table("orders", mdt,
                             sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                             sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                               nullable=False),
                             sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'),
                                               nullable=False),
                             sqlalchemy.Column("date", sqlalchemy.DateTime(), default=datetime.datetime.now()),
                             sqlalchemy.Column("order_status",
                                               sqlalchemy.String(50)), 
                            )               

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False})
mdt.create_all(engine)

