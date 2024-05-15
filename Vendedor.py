import sqlite3
from datetime import datetime

class Vendedor:
    def __init__(self, nome, cpf, data_nascimento, email, estado):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.estado = estado

class GerenciarVendedor:
    def __init__(self, db_name="vendedores.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS vendedores (
                                cpf CHAR(11) PRIMARY KEY,
                                nome VARCHAR(100) NOT NULL,
                                data_nascimento TEXT NOT NULL,
                                email VARCHAR(100) NOT NULL UNIQUE,
                                estado CHAR(2) NOT NULL)''')

    def create_vendedor(self, vendedor):
        with self.conn:
            self.conn.execute("INSERT INTO vendedores (cpf, nome, data_nascimento, email, estado) VALUES (?, ?, ?, ?, ?)",
                              (vendedor.cpf, vendedor.nome, vendedor.data_nascimento, vendedor.email, vendedor.estado))

    def read_vendedor(self, cpf):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM vendedores WHERE cpf = ?", (cpf,))
        return cur.fetchone()

    def update_vendedor(self, vendedor):
        with self.conn:
            self.conn.execute("UPDATE vendedores SET nome = ?, data_nascimento = ?, email = ?, estado = ? WHERE cpf = ?",
                              (vendedor.nome, vendedor.data_nascimento, vendedor.email, vendedor.estado, vendedor.cpf))

    def delete_vendedor(self, cpf):
        with self.conn:
            self.conn.execute("DELETE FROM vendedores WHERE cpf = ?", (cpf,))

    def read_all_vendedores(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM vendedores")
        return cur.fetchall()
