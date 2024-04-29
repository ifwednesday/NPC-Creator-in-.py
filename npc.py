import tkinter as tk
from tkinter import ttk
from editor_npc import EditorNPC  # Importe a classe EditorNPC
from comprar import Comprar  # Importe a aba de comprar
from vender import Vender  # Importe a aba de vender

class EditorLuaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Editor de Lua")
        self.geometry("400x300")
        
        # Criação das abas
        self.tabControl = ttk.Notebook(self)
        
        # Adiciona a aba Editor de NPC
        self.tab_npc = EditorNPC(self.tabControl)
        self.tabControl.add(self.tab_npc, text="Editor de NPC")
        
        # Adiciona a aba Comprar
        self.tab_comprar = Comprar(self.tabControl)
        self.tabControl.add(self.tab_comprar, text="Comprar")
        
        # Adiciona a aba Vender
        self.tab_vender = Vender(self.tabControl)
        self.tabControl.add(self.tab_vender, text="Vender")
        
        self.tabControl.pack(expand=1, fill="both")

if __name__ == "__main__":
    app = EditorLuaApp()
    app.mainloop()
