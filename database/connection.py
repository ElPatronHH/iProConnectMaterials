from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select

db = create_engine('mysql+mysqlconnector://root@localhost/iproconnectmaterials')

metadata = MetaData()

stock_table = Table(
    "stock",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("descripcion", String),
    Column("numParte", Integer),
    Column("currentStock", Integer),
    Column("maxVenta", Integer),
    Column("minVenta", Integer),
    Column("puntoMax", Integer),
    Column("puntoReorden", Integer),
)

conexion = db.connect()