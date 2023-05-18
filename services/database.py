import mysql.connector

#inicializando conexao 
cnxn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '40218312Ni.',
    database = 'bd_academia',
)

#executa comandos da conexao 
cursor = cnxn.cursor()

