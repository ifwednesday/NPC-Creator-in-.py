import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Importe diretamente a função messagebox

import xml.etree.ElementTree as ET

class Comprar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.lista_compras = []  # Lista para armazenar os itens de compra
        
        # Criar widgets
        self.lbl_item = tk.Label(self, text="Item:")
        self.ent_item = tk.Entry(self)
        
        self.lbl_preco = tk.Label(self, text="Preço:")
        self.ent_preco = tk.Entry(self)
        
        self.btn_adicionar = tk.Button(self, text="Adicionar à Lista", command=self.adicionar_item)
        
        self.frame_checklists = tk.Frame(self)
        self.frame_checklist_disponiveis = tk.Frame(self.frame_checklists)
        self.frame_checklist_adicionados = tk.Frame(self.frame_checklists)
        
        self.lista_box = tk.Listbox(self.frame_checklist_adicionados, width=30, height=10)
        self.btn_remover = tk.Button(self.frame_checklist_adicionados, text="Remover Selecionado", command=self.remover_item)
        
        self.lbl_disponiveis = tk.Label(self.frame_checklist_disponiveis, text="Itens Disponíveis:")
        self.lista_disponiveis = tk.Listbox(self.frame_checklist_disponiveis, width=30, height=10)
        
        # Layout dos widgets
        self.lbl_item.grid(row=0, column=0, sticky="w")
        self.ent_item.grid(row=0, column=1)
        self.lbl_preco.grid(row=1, column=0, sticky="w")
        self.ent_preco.grid(row=1, column=1)
        self.btn_adicionar.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.frame_checklists.grid(row=3, column=0, columnspan=2)
        self.frame_checklist_disponiveis.grid(row=0, column=0, padx=10)
        self.frame_checklist_adicionados.grid(row=0, column=1, padx=10)
        
        self.lista_box.pack(side=tk.TOP, padx=10, pady=5)
        self.btn_remover.pack(side=tk.BOTTOM, padx=10, pady=5)
        
        self.lbl_disponiveis.pack(side=tk.TOP, padx=10, pady=5)
        self.lista_disponiveis.pack(side=tk.TOP, padx=10, pady=5)
        
        # Carregar itens disponíveis do arquivo XML
        self.carregar_itens_disponiveis()
        
        # Adicionar evento de digitação para filtrar itens disponíveis
        self.ent_item.bind("<KeyRelease>", self.filtrar_itens_disponiveis)
        
    def adicionar_item(self):
        item_selecionado = self.lista_disponiveis.curselection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item da lista disponível.")
            return

        item_text = self.lista_disponiveis.get(item_selecionado)
        item_id = item_text.split("(ID: ")[1][:-1]  # Extrair o ID do texto
        item_name = item_text.split(" (ID: ")[0]

        preco = self.ent_preco.get()
        if not preco:
            messagebox.showwarning("Aviso", "Digite um valor para o preço.")
            return

        self.lista_compras.append((item_name, item_id, preco))
        self.atualizar_lista()
        self.ent_item.delete(0, tk.END)
        self.ent_preco.delete(0, tk.END)
        
    def remover_item(self):
        selecionado = self.lista_box.curselection()
        if selecionado:
            indice = selecionado[0]
            del self.lista_compras[indice]
            self.atualizar_lista()
        
    def atualizar_lista(self):
        self.lista_box.delete(0, tk.END)
        for item_name, item_id, preco in self.lista_compras:
            self.lista_box.insert(tk.END, f"{item_name} (ID: {item_id}) - R${preco}")
    
    def carregar_itens_disponiveis(self):
        # Parse do arquivo XML
        tree = ET.parse("items.xml")
        root = tree.getroot()
        
        # Limpa a lista de itens disponíveis antes de atualizar
        self.lista_disponiveis.delete(0, tk.END)
        
        # Adiciona os itens disponíveis na lista
        self.itens_disponiveis = []
        for item in root.findall("item"):
            item_id = item.get("id")
            item_name = item.get("name")
            if item_id is not None and item_name is not None:  # Verifica se item_id e item_name não são None
                self.itens_disponiveis.append((item_id, item_name))
                self.lista_disponiveis.insert(tk.END, f"{item_name} (ID: {item_id})")
    
    def filtrar_itens_disponiveis(self, event):
        # Filtra os itens disponíveis de acordo com o que o usuário digita
        filtro = self.ent_item.get().lower()
        self.lista_disponiveis.delete(0, tk.END)
        for item_id, item_name in self.itens_disponiveis:
            if item_name is not None and item_id is not None and (filtro in item_name.lower() or filtro in item_id):
                self.lista_disponiveis.insert(tk.END, f"{item_name} (ID: {item_id})")
