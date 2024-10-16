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

import customtkinter as ctk
from tkinter import END
from PIL import Image
import os
from database import Banco_de_Dados

# iniciando a aplicação
class App(ctk.CTk, Banco_de_Dados):
    def __init__(self):
        super().__init__()
        self.db = Banco_de_Dados()
        self.self_mainconfig()
        self.cad_frame = None
        self.login_page()
        self.db.db_create_table()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    # config da janela principal
    def self_mainconfig(self):  
        self.geometry("800x500")
        self.title("Sistema de login")
        self.resizable(height=False, width=False)
        self._set_appearance_mode("black")

    def on_closing(self):
        self.db.db_disconnect()
        self.destroy()

    def login_page(self):
        # verifica se existe uma tela de cadastro e deleta se existir após o botão de cadastro ser clicado
        if self.cad_frame is not None:
            for widget in self.cad_frame.winfo_children():
                widget.destroy()
            self.cad_frame.destroy()
            self.label_cad_img.destroy()
        
        # caminho da imagem
        current_dir = os.path.dirname(__file__)
        image_dir = os.path.join(current_dir, "../static/image")
        image_path = os.path.join(image_dir, "login.png")
        ## abrindo a imagem
        self.img = ctk.CTkImage(light_image=Image.open(image_path),
                                dark_image=Image.open(image_path),
                                size=(440, 480))
        self.label_img = ctk.CTkLabel(self, image=self.img, text=None)
        self.label_img.place(x=0, y=30)

        # Titulo em label
        self.title = ctk.CTkLabel(self, text="Sistema de login e cadastro com Python",
                                    font=('Century Gothic bold', 30))          
        self.title.place(x=125, y=15)

        # Frame do formulário de login
        self.login_frame = ctk.CTkFrame(self, width=355, height=455)
        self.login_frame.place(x=440, y=110)

        # widgets no frame 
        self.label_title = ctk.CTkLabel(self.login_frame, text="Faça seu login", font=('Century Gothic bold', 22))
        self.label_title.grid(row=0, column=0, pady=10, padx=10)

        # entrada do nome de usuario
        self.username_entry_log = ctk.CTkEntry(self.login_frame, width=300, 
                                                placeholder_text="Escreva seu nome de usuário...".capitalize(),
                                                font=('Century Gothic bold', 12),
                                                corner_radius=15,
                                                border_color="#317bf1",
                                                border_width=2)
        self.username_entry_log.grid(row=1, column=0, padx=10, pady=10)

        # entrada da senha do usuario
        self.userpassword_entry_log = ctk.CTkEntry(self.login_frame, width=300,
                                                    placeholder_text="Escreva sua senha...".capitalize(),
                                                    font=('Century Gothic', 12),
                                                    corner_radius=14,
                                                    border_width=2,
                                                    border_color="#317bf1",
                                                    show="*")
        self.userpassword_entry_log.grid(row=2, column=0, padx=10, pady=10)

        # mostrar senha ou não
        self.show_password_login = ctk.CTkCheckBox(self.login_frame, 
                                                    text="Mostrar senha".capitalize(),
                                                    font=('Century Gothic', 14),
                                                    corner_radius=14,
                                                    fg_color="#317bf1",
                                                    command=self.password_log_visualization)
        self.show_password_login.grid(row=3, column=0, pady=10)

        # botão de login
        self.login_btn = ctk.CTkButton(self.login_frame, width=200,
                                        text="Fazer login".upper(), 
                                        font=('Century Gothic bold', 15),
                                        corner_radius=18,
                                        fg_color="#317bf1",
                                        command=self.login_validation)
        self.login_btn.grid(row=4, column=0, padx=10, pady=10)

        # mensgem p/acc nova
        self.under_span = ctk.CTkLabel(self.login_frame, text="Ou crie sua conta nova agora\n gratuitamente apertando no botão abaixo!",
                                        font=('Century Gothic bold', 12))
        self.under_span.grid(row=5, column=0, padx=10, pady=10)

        # botão de cadastro
        self.signup_btn = ctk.CTkButton(self.login_frame, width=150,
                                        text="Cadastrar-se".upper(),
                                        font=('Century Gothic bold', 15),
                                        corner_radius=18,
                                        fg_color="#317bf1",
                                        hover_color="#0d59a5",
                                        command=self.tela_cadastro)
        self.signup_btn.grid(row=6, column=0, padx=10, pady=10)


    def password_log_visualization(self):
        if self.show_password_login.get() == True:
            self.userpassword_entry_log.configure(show="")
        else:
            self.userpassword_entry_log.configure(show="*")

    def clear_login_entry(self):
        self.username_entry_log.delete(0, END)
        self.userpassword_entry_log.delete(0, END)

    def tela_cadastro(self):
        # del na tela de login e nova dela de cadastro
        self.title.place_forget()
        self.login_frame.place_forget()
        self.under_span.place_forget()
        self.signup_btn.place_forget()
        
        # caminho da imagem de cadastro
        current_cad_dir = os.path.dirname(__file__)
        image_cad_dir = os.path.join(current_cad_dir, "../static/image")
        image_cad_path = os.path.join(image_cad_dir, "Signup.png")
        ## abrindo a imagem de cadastro
        self.cad_img = ctk.CTkImage(light_image=Image.open(image_cad_path),
                                    dark_image=Image.open(image_cad_path),
                                    size=(420, 460))
        self.label_cad_img = ctk.CTkLabel(self, image=self.cad_img, text=None)
        self.label_cad_img.place(x=0, y=3)

        # Frame da tela de cadastro
        self.cad_frame = ctk.CTkFrame(self, width=355, height=550)
        self.cad_frame.place(x=440, y=75)

        # Titulo do frame do novo usuario 
        self.label_cad_title = ctk.CTkLabel(self.cad_frame, text="Faça seu cadastro", font=('Century Gothic bold', 22))
        self.label_cad_title.grid(row=0, column=0, pady=10, padx=10)

        # nome do novo usuario
        self.username_entry_cad = ctk.CTkEntry(self.cad_frame, width=300, 
                                                placeholder_text="Escreva seu nome de usuário...".capitalize().strip(),
                                                font=('Century Gothic bold', 12),
                                                corner_radius=15,
                                                border_color="#317bf1",
                                                border_width=2)
        self.username_entry_cad.grid(row=1, column=0, padx=10, pady=10)

        # email do novo usuario
        self.useremail_entry_cad = ctk.CTkEntry(self.cad_frame, width=300, 
                                                placeholder_text="Escreva seu Email de usuário...".capitalize().strip(),
                                                font=('Century Gothic bold', 12),
                                                corner_radius=15,
                                                border_color="#317bf1",
                                                border_width=2)
        self.useremail_entry_cad.grid(row=2, column=0, padx=10, pady=10)

        # senha do novo usuario
        self.userpassword_entry_cad = ctk.CTkEntry(self.cad_frame, width=300,
                                                    placeholder_text="Escreva sua senha...".capitalize().strip(),
                                                    font=('Century Gothic', 12),
                                                    corner_radius=14,
                                                    border_width=2,
                                                    border_color="#317bf1",
                                                    show="*")
        self.userpassword_entry_cad.grid(row=3, column=0, padx=10, pady=10)

        # confirmar senha do novo usuario                                 
        self.userpassword_entry_cad_conf = ctk.CTkEntry(self.cad_frame, width=300,
                                                        placeholder_text="Confirme sua senha...".capitalize().strip(),
                                                        font=('Century Gothic', 12),
                                                        corner_radius=14,
                                                        border_width=2,
                                                        border_color="#317bf1",
                                                        show="*")
        self.userpassword_entry_cad_conf.grid(row=4, column=0, padx=10, pady=10)

        # mostrar senha ou não do novo usuario
        self.show_cad_password = ctk.CTkCheckBox(self.cad_frame, 
                                                text="Mostrar senha".capitalize(),
                                                font=('Century Gothic', 14),
                                                corner_radius=14,
                                                fg_color="#317bf1",
                                                command=self.password_cad_visualization)
        self.show_cad_password.grid(row=5, column=0, pady=5)

        # botão de cadastro
        self.cad_btn = ctk.CTkButton(self.cad_frame, width=200,
                                    text="Fazer cadastro".upper(), 
                                    font=('Century Gothic bold', 15),
                                    corner_radius=18,
                                    fg_color="#317bf1",
                                    command=self.cad_new_user)
        self.cad_btn.grid(row=6, column=0, padx=10, pady=10)     


        self.back_to_login_btn = ctk.CTkButton(self.cad_frame, width=110,
                                    text="Voltar a tela de login".upper(), 
                                    font=('Century Gothic bold', 12),
                                    corner_radius=18,
                                    fg_color="#317bf1",
                                    command=self.login_page)
        self.back_to_login_btn.grid(row=7, column=0, padx=10, pady=10)                                             

    # limpar os campos de cadastro após a confirmação do cadastro
    def clear_cad_entry(self):
        self.username_entry_cad.delete(0, END)
        self.useremail_entry_cad.delete(0, END)
        self.userpassword_entry_cad.delete(0, END)
        self.userpassword_entry_cad_conf.delete(0, END)

    def password_cad_visualization(self):
        if self.show_cad_password.get() == True:
            self.userpassword_entry_cad.configure(show="")
            self.userpassword_entry_cad_conf.configure(show="")
        else:
            self.userpassword_entry_cad.configure(show="*")
            self.userpassword_entry_cad_conf.configure(show="*")

if __name__ == "__main__":
    app = App()
    app.mainloop()
