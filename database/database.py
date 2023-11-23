from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configura la cadena de conexión para la base de datos de Azure
# Reemplaza 'topicos' con tu nombre de usuario y 'Admin12345' con tu contraseña
URL_DATABASE = 'mysql+mysqlconnector://topicos:Admin12345@iproconnectdb.mysql.database.azure.com:3306/iproconnectmaterials'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DataBase = declarative_base()
