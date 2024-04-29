import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

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
        
    def salvar(self):
        # Abrir uma janela de diálogo para salvar o arquivo .lua
        filename = filedialog.asksaveasfilename(defaultextension=".lua", filetypes=[("Arquivos Lua", "*.lua")])
        
        # Verificar se o usuário cancelou a operação de salvamento
        if filename == "":
            return
        
        # Ler o conteúdo do arquivo NPC principal
        npc_filename = "npc_principal.lua"
        with open(npc_filename, "r") as f:
            npc_lines = f.readlines()

        # Modificar as entradas editadas
        lines = npc_lines[:]
        if self.ent_internalNpcName.get():
            lines[0] = f"local internalNpcName = '{self.ent_internalNpcName.get()}'\n"
        if self.ent_lookType.get():
            lines[9] = f"lookType = {self.ent_lookType.get()}\n"
        if self.ent_lookHead.get():
            lines[10] = f"lookHead = {self.ent_lookHead.get()}\n"
        if self.ent_lookBody.get():
            lines[11] = f"lookBody = {self.ent_lookBody.get()}\n"
        if self.ent_lookLegs.get():
            lines[12] = f"lookLegs = {self.ent_lookLegs.get()}\n"
        if self.ent_lookFeet.get():
            lines[13] = f"lookFeet = {self.ent_lookFeet.get()}\n"
        if self.ent_lookAddons.get():
            lines[14] = f"lookAddons = {self.ent_lookAddons.get()}\n"

        # Salvar as alterações
        with open(filename, "w") as f:
            f.writelines(lines)
        print("Alterações salvas com sucesso!")

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

if __name__ == "__main__":
    app = EditorLuaApp()
    app.mainloop()
