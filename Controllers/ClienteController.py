import services.database as db

def incluir(cliente):
    query = """INSERT INTO infos (nome, idade, sexo, senha) 
               VALUES (%s, %s, %s, %s)"""
    values = (cliente.nome, cliente.idade, cliente.sexo, cliente.senha)

    cursor = db.cnxn.cursor()
    cursor.execute(query, values)
    count = cursor.rowcount

    db.cnxn.commit()

def login(nome, senha):
    query = "SELECT * FROM infos WHERE nome = %s AND senha = %s"
    values = (nome, senha)

    cursor = db.cnxn.cursor()
    cursor.execute(query, values)
    result = cursor.fetchone()

    if result:
        return result  # Retorna o registro completo do usuário
    else:
        return None

def adicionar_treino(day, muscle_group, exercise, sets, reps, client_id):
    query = """INSERT INTO t_treino (dia, musculo, exercicio, serie, repeticao, cliente_id) 
               VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (day, muscle_group, exercise, sets, reps, client_id)

    cursor = db.cnxn.cursor()
    cursor.execute(query, values)
    count = cursor.rowcount

    db.cnxn.commit()

def alterar_treino(day, muscle_group, exercise, sets, reps, client_id,idt_treino):
    query = """
    UPDATE t_treino 
    SET dia = %s, musculo = %s, exercicio = %s, serie = %s, repeticao = %s, cliente_id = %s
    WHERE idt_treino = %s
    """
    values = (day, muscle_group, exercise, sets, reps, client_id, idt_treino)

    cursor = db.cnxn.cursor()
    cursor.execute(query, values)
    count = cursor.rowcount

    db.cnxn.commit()

def Excluir(idC):
    query = "DELETE FROM t_treino WHERE idt_treino = %s"
    values = (idC,)

    cursor = db.cnxn.cursor()
    cursor.execute(query, values)
    count = cursor.rowcount

    db.cnxn.commit()

def listar_treinos_salvos(client_id):
    query = "SELECT idt_treino, dia, musculo, exercicio, serie, repeticao FROM t_treino WHERE cliente_id = %s"
    values = (client_id,)

    cursor = db.cnxn.cursor()
    cursor.execute(query, values)
    result = cursor.fetchall()

    return result

def treinos_salvos(idt_treino):
    query = "SELECT * FROM t_treino WHERE idt_treino = %s"
    values = (idt_treino,)
    treino = None

    cursor = db.cnxn.cursor()
    cursor.execute(query, values)
    result = cursor.fetchone()

    if result:
        treino = {
            'id': result[0],
            'dia': result[1],
            'musculo': result[2],
            'exercicio': result[3],
            'serie': result[4],
            'repeticao': result[5],
            'cliente_id': result[6]
        }

    return treino



