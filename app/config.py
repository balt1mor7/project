import os
SECRET_KEY = "B73kPosw8aad881ld234qer56s78da91ndm597bba30b8c60fad7f59a98d22"
params = {
    "username": "root",
    "password": "Pa$$w0rd",
    "db_name": "test"
}
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{params.get("username")}:{params.get("password")}@localhost/{params.get("db_name")}'
