# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3
import hashlib
from tkinter import messagebox

class Banco_de_Dados():
    def conection_db(self):
        # criando e conectando o banco de dados
        self.conn = sqlite3.connect("users_database.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado com êxito!")
    
    def db_disconnect(self):
        # desconectando o banco de dados
        self.conn.close()
        print("Banco de dados desconectado com êxito!")

    def db_create_table(self):
        # criação, configuração e commit da tabela
        self.conection_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                UserEmail TEXT NOT NULL,
                UserPassword TEXT NOT NULL,
                UserPasswordConf TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela criada e comitada com sucesso!") 
        self.db_disconnect()

        # criptografando as senhas
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def cad_new_user(self):
        # Salvando os dados em váriaveis, criptografando as senhas, se conectando ao banco de dados e testando falhas
        self.cad_username_entry_get = getattr(self, "username_entry_cad").get()
        self.cad_useremail_entry_get = getattr(self, "useremail_entry_cad").get()
        self.cad_userpassword_entry_get = getattr(self, "userpassword_entry_cad").get()
        self.cad_userpassword_conf_entry_get = getattr(self, "userpassword_entry_cad_conf").get()

        hashed_password = self.hash_password(self.cad_userpassword_entry_get)
        hashed_password_conf = self.hash_password(self.cad_userpassword_conf_entry_get)

        self.conection_db()
        
        try:
            # Verificando se os dados foram inseridos corretamente
            if (self.cad_username_entry_get == "" 
                or self.cad_useremail_entry_get == ""
                or self.cad_userpassword_entry_get == ""
                or self.cad_userpassword_conf_entry_get == ""):
                messagebox.showerror(title="Erro 001",
                                    message="Favor, preencha todos os campos com as devidas informações!")
                return
                
            if (len(self.cad_username_entry_get) < 4):
                messagebox.showerror(title="Erro 002", 
                                    message="O seu nome de usuário deve conter pelo menos 4 caracteres!")
                return

            if (self.cad_userpassword_entry_get != self.cad_userpassword_conf_entry_get):
                messagebox.showerror(title="Erro 003", 
                                    message="As senhas inseridas devem ser iguais!\nFavor, confirme as senhas novamente.")
                return
                
            if (len(self.cad_userpassword_entry_get) < 5):
                messagebox.showerror(title="Erro 004", 
                                    message="As senhas devem conter pelo menos 5 caracteres!")
                return
            
            # Verificando se o nome de usuário existe
            self.cursor.execute("SELECT * FROM users WHERE Username = ?", (self.cad_username_entry_get,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                messagebox.showerror(title="Erro 005",
                                    message="O nome de usuário inserido já existe!\nFavor, escolha outro nome de usuário.")
                return

            # Verificando se o email existe
            self.cursor.execute("SELECT * FROM users WHERE UserEmail = ?", (self.cad_useremail_entry_get,))
            existing_email = self.cursor.fetchone()

            if existing_email:
                messagebox.showerror(title="Erro 008",
                                    message="O email inserido já está em uso!\nFavor, faça login ou escolha outro email.")
                return

            # Inserindo os dados na tabela se não ouver nenhum erro
            self.cursor.execute("""
                INSERT INTO users (Username, UserEmail, UserPassword, UserPasswordConf)
                VALUES (?, ?, ?, ?)""", (self.cad_username_entry_get,
                                        self.cad_useremail_entry_get,
                                        hashed_password,
                                        hashed_password_conf))
            
            self.conn.commit()
            self.clear_cad_entry()
            self.login_page()
            messagebox.showinfo(title="Sucesso!",
                                message=f"Seu usuário '{self.cad_username_entry_get}' foi criado com sucesso!")
                
        except sqlite3.Error as e:
            print("Erro no banco de dados", e)
            messagebox.showerror(title="Erro 006",
                                message="Ocorreu um erro no banco de dados!\nFavor, tente novamente.")
            
        except Exception as e:
            print("Erro inesperado no sistema", e)
            messagebox.showerror(title="Erro 007",
                                message="Ocorreu um erro inesperado no sistema!\nFavor, tente novamente.")
            
        finally:
            self.db_disconnect()
            

    def login_validation(self):
        # armazenando os dados das entrys de login numa váriavel
        self.get_username_login = self.username_entry_log.get()
        self.get_password_login = self.userpassword_entry_log.get()

        # aplicando uma hash as senhas de login
        hashed_password_login = self.hash_password(self.get_password_login)

        # se conectando ao banco de dados
        self.conection_db()
        self.cursor.execute("""SELECT * FROM users WHERE (Username = ? AND UserPassword = ?)""", 
                            (self.get_username_login, hashed_password_login))
        
        # verificando se os dados existem
        self.validacao_dos_dados = self.cursor.fetchone()

        # verificando se as informações das entrys existem e se estão corretas no banco de dados
        if self.validacao_dos_dados:
                messagebox.showinfo(title="Sucesso no login!",
                                    message="Seu login foi efetuado com sucesso!")
                self.db_disconnect()
                self.clear_login_entry()
        else:
                messagebox.showerror(title="Erro 005",
                                    message="Seus dados são inválidos ou inexistentes!\nVerifique se as informações inseridas estão corretas e tente novamente!")
                self.db_disconnect()
