import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import shutil
import xml.etree.ElementTree as ET

class EditorNPC(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Criar widgets
        self.lbl_internalNpcName = tk.Label(self, text="Nome Interno do NPC:")
        self.ent_internalNpcName = tk.Entry(self)
        
        self.lbl_lookType = tk.Label(self, text="lookType:")
        self.ent_lookType = tk.Entry(self)
        
        self.lbl_lookHead = tk.Label(self, text="lookHead:")
        self.ent_lookHead = tk.Entry(self)
        
        self.lbl_lookBody = tk.Label(self, text="lookBody:")
        self.ent_lookBody = tk.Entry(self)
        
        self.lbl_lookLegs = tk.Label(self, text="lookLegs:")
        self.ent_lookLegs = tk.Entry(self)
        
        self.lbl_lookFeet = tk.Label(self, text="lookFeet:")
        self.ent_lookFeet = tk.Entry(self)
        
        self.lbl_lookAddons = tk.Label(self, text="lookAddons:")
        self.ent_lookAddons = tk.Entry(self)
        
        self.btn_salvar = tk.Button(self, text="Salvar", command=self.salvar)
        
        # Layout dos widgets
        self.lbl_internalNpcName.grid(row=0, column=0, sticky="w")
        self.ent_internalNpcName.grid(row=0, column=1)
        self.lbl_lookType.grid(row=1, column=0, sticky="w")
        self.ent_lookType.grid(row=1, column=1)
        self.lbl_lookHead.grid(row=2, column=0, sticky="w")
        self.ent_lookHead.grid(row=2, column=1)
        self.lbl_lookBody.grid(row=3, column=0, sticky="w")
        self.ent_lookBody.grid(row=3, column=1)
        self.lbl_lookLegs.grid(row=4, column=0, sticky="w")
        self.ent_lookLegs.grid(row=4, column=1)
        self.lbl_lookFeet.grid(row=5, column=0, sticky="w")
        self.ent_lookFeet.grid(row=5, column=1)
        self.lbl_lookAddons.grid(row=6, column=0, sticky="w")
        self.ent_lookAddons.grid(row=6, column=1)
        self.btn_salvar.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Lista de compras e vendas
        self.lista_compras = []
        self.lista_vendas = []
        
    def salvar(self):
        # Lógica para salvar as configurações do NPC
        npc_name = self.ent_internalNpcName.get()
        look_type = self.ent_lookType.get()
        look_head = self.ent_lookHead.get()
        look_body = self.ent_lookBody.get()
        look_legs = self.ent_lookLegs.get()
        look_feet = self.ent_lookFeet.get()
        look_addons = self.ent_lookAddons.get()

        if not npc_name:
            print("Nome interno do NPC é obrigatório.")
            return
        
        # Selecionar o local para salvar o novo arquivo
        filename = filedialog.asksaveasfilename(defaultextension=".lua", filetypes=[("Lua files", "*.lua")])
        if not filename:
            print("Nenhum local selecionado.")
            return
        
        # Copiar o arquivo modelo npc_principal.lua para o novo arquivo
        try:
            shutil.copy("npc_principal.lua", filename)
        except Exception as e:
            print(f"Erro ao copiar o arquivo modelo: {e}")
            return
        
        # Ler o novo arquivo
        try:
            with open(filename, "r") as f:
                npc_lines = f.readlines()
        except Exception as e:
            print(f"Erro ao ler o novo arquivo: {e}")
            return
        
        # Modificar o nome do NPC e o bloco npcConfig.outfit
        for i, line in enumerate(npc_lines):
            if "local internalNpcName" in line:
                npc_lines[i] = f'local internalNpcName = "{npc_name}"\n'
            if "npcConfig.outfit = {" in line:
                npc_lines[i+1] = f'\tlookType = {look_type},\n'
                npc_lines[i+2] = f'\tlookHead = {look_head},\n'
                npc_lines[i+3] = f'\tlookBody = {look_body},\n'
                npc_lines[i+4] = f'\tlookLegs = {look_legs},\n'
                npc_lines[i+5] = f'\tlookFeet = {look_feet},\n'
                npc_lines[i+6] = f'\tlookAddons = {look_addons},\n'
        
        # Procurar e modificar o bloco npcConfig.shop
        shop_start = -1
        shop_end = -1
        for i, line in enumerate(npc_lines):
            if "npcConfig.shop = {" in line:
                shop_start = i
            elif "}" in line and shop_start != -1:
                shop_end = i
                break
        
        if shop_start != -1 and shop_end != -1:
            # Limpar as linhas existentes dentro do bloco shop
            del npc_lines[shop_start + 1:shop_end]
            
            # Adicionar os itens de compra e venda
            for compra in self.lista_compras:
                npc_lines.insert(shop_start + 1, f'\t{{ itemName = "{compra[0]}", clientId = {compra[1]}, buy = {compra[2]} }},\n')
            for venda in self.lista_vendas:
                npc_lines.insert(shop_start + 1 + len(self.lista_compras), f'\t{{ itemName = "{venda[0]}", clientId = {venda[1]}, sell = {venda[2]} }},\n')
        
        # Salvar as alterações
        try:
            with open(filename, "w") as f:
                f.writelines(npc_lines)
            print("Alterações salvas com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")

class Comprar(tk.Frame):
    def __init__(self, parent, editor):
        super().__init__(parent)
        
        self.editor = editor  # Referência ao editor principal
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
        self.lista_disponiveis.pack(side=tk.BOTTOM, padx=10, pady=5)
        
        # Carregar itens disponíveis
        self.carregar_itens_disponiveis()
        
        # Bind do evento de filtro
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
        self.editor.lista_compras.append((item_name, item_id, preco))  # Adicionar à lista no editor principal
        self.atualizar_lista()
        self.ent_item.delete(0, tk.END)
        self.ent_preco.delete(0, tk.END)
        
    def remover_item(self):
        selecionado = self.lista_box.curselection()
        if selecionado:
            indice = selecionado[0]
            del self.lista_compras[indice]
            del self.editor.lista_compras[indice]  # Remover da lista no editor principal
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
            if item_id is not None and item_name is not None:
                self.itens_disponiveis.append((item_id, item_name))
                self.lista_disponiveis.insert(tk.END, f"{item_name} (ID: {item_id})")
    
    def filtrar_itens_disponiveis(self, event):
        # Filtra os itens disponíveis de acordo com o que o usuário digita
        filtro = self.ent_item.get().lower()
        self.lista_disponiveis.delete(0, tk.END)
        for item_id, item_name in self.itens_disponiveis:
            if filtro in item_name.lower() or filtro in item_id:
                self.lista_disponiveis.insert(tk.END, f"{item_name} (ID: {item_id})")

class Vender(tk.Frame):
    def __init__(self, parent, editor):
        super().__init__(parent)
        
        self.editor = editor  # Referência ao editor principal
        self.lista_vendas = []  # Lista para armazenar os itens de venda
        
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
        self.lista_disponiveis.pack(side=tk.BOTTOM, padx=10, pady=5)
        
        # Carregar itens disponíveis
        self.carregar_itens_disponiveis()
        
        # Bind do evento de filtro
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
        
        self.lista_vendas.append((item_name, item_id, preco))
        self.editor.lista_vendas.append((item_name, item_id, preco))  # Adicionar à lista no editor principal
        self.atualizar_lista()
        self.ent_item.delete(0, tk.END)
        self.ent_preco.delete(0, tk.END)
        
    def remover_item(self):
        selecionado = self.lista_box.curselection()
        if selecionado:
            indice = selecionado[0]
            del self.lista_vendas[indice]
            del self.editor.lista_vendas[indice]  # Remover da lista no editor principal
            self.atualizar_lista()
        
    def atualizar_lista(self):
        self.lista_box.delete(0, tk.END)
        for item_name, item_id, preco in self.lista_vendas:
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
            if item_id is not None and item_name is not None:
                self.itens_disponiveis.append((item_id, item_name))
                self.lista_disponiveis.insert(tk.END, f"{item_name} (ID: {item_id})")
    
    def filtrar_itens_disponiveis(self, event):
        # Filtra os itens disponíveis de acordo com o que o usuário digita
        filtro = self.ent_item.get().lower()
        self.lista_disponiveis.delete(0, tk.END)
        for item_id, item_name in self.itens_disponiveis:
            if filtro in item_name.lower() or filtro in item_id:
                self.lista_disponiveis.insert(tk.END, f"{item_name} (ID: {item_id})")

class EditorLuaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Editor Lua")
        
        self.tabControl = ttk.Notebook(self)
        self.tab_editor_npc = tk.Frame(self.tabControl)
        self.tab_comprar = tk.Frame(self.tabControl)
        self.tab_vender = tk.Frame(self.tabControl)
        
        self.tabControl.add(self.tab_editor_npc, text="Editor de NPC")
        self.tabControl.add(self.tab_comprar, text="Compras")
        self.tabControl.add(self.tab_vender, text="Vendas")
        
        self.tabControl.pack(expand=1, fill="both")
        
        self.editor_npc = EditorNPC(self.tab_editor_npc)
        self.editor_npc.pack()
        
        self.comprar = Comprar(self.tab_comprar, self.editor_npc)
        self.comprar.pack()
        
        self.vender = Vender(self.tab_vender, self.editor_npc)
        self.vender.pack()

if __name__ == "__main__":
    app = EditorLuaApp()
    app.mainloop()
