import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

#______________________________________________VENTANA____________________________________________________
        self.title("Calculadora y graficadora de limites")
        self.geometry("1200x720")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

#_____________________________________ADAPTADOR DE TAMAÑO__________________________________________________
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


#_______________________________________PESTAÑAS__________________________________________________________
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

#_________________________________________CREACION______________________________________________
        self.tab_inicio = self.tabs.add("Inicio")
        self.tab_Infinito = self.tabs.add("Infinito")
        self.tab_Trigonometricos = self.tabs.add("Trigonometricos")
        self.tab_laterales = self.tabs.add("Laterales")
        self.tab_Tendenciainfinita = self.tabs.add("Tendenciainfinita")
        self.tab_Infinitoyradicales = self.tabs.add("Infinitoyradicales")

        self.crear_inicio()
        self.crear_Infinito()
        self.crear_Trigonometricos()
        self.crear_Laterales()
        self.crear_Tendenciainfinita()
        self.crear_Infinitoyradicales()

#__________________________________________INICIO________________________________________________________

    def crear_inicio(self):
        #________________________________Título__________________________________________________________
        titulo = ctk.CTkLabel(
            self.tab_inicio,
            text="Calculadora de Cálculo Básico",
            font=("Arial", 32, "bold")
        )
        titulo.pack(pady=(50, 10))

        
        subtitulo = ctk.CTkLabel(
            self.tab_inicio,
            text="Programa para resolver y graficar distintos tipos de límites",
            font=("Arial", 16),
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 40))

        #_______________________________________Texto explicativo___________________________________
        texto_ayuda = (
            "Usa las pestañas de arriba para moverte entre las diferentes secciones.\n"
            "En cada una podrás ingresar la función matemática que necesites, "
            "calcular su límite y ver su comportamiento en el gráfico de la derecha."
        )
        
        lbl_explicacion = ctk.CTkLabel(
            self.tab_inicio,
            text=texto_ayuda,
            font=("Arial", 15),
            justify="center",
            wraplength=800  
        )
        lbl_explicacion.pack(pady=30)

       
        lbl_hecho_por = ctk.CTkLabel(
            self.tab_inicio,
            text="Creado por:",
            font=("Arial", 14, "bold"),
            text_color="#3b8ed0"
        )
        lbl_hecho_por.pack(pady=(40, 5))

        integrantes = "Benjamin Varela  |  Benjamin Riquelme  |  Diego Manquicoy  |  Joaquin Carrillo"
        lbl_integrantes = ctk.CTkLabel(
            self.tab_inicio,
            text=integrantes,
            font=("Arial", 14)
        )
        lbl_integrantes.pack()

#____________________________________CREARFIGURAS________________________________________________________
    def crear_canvas(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        eje = figura.add_subplot(111)
        
        # Diseño oscuro 
        figura.patch.set_facecolor('#242424')
        eje.set_facecolor('#1a1a1a')
        eje.tick_params(colors='white')
        eje.grid(True, color='#444444')
        
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas
    

#________________________________________INFINITO_________________________________________________________

    def crear_Infinito(self):
        frame_controles = ctk.CTkFrame(self.tab_Infinito, width=300)
        frame_controles.pack(side="left", fill="y", padx=10, pady=10)
        
        frame_grafico = ctk.CTkFrame(self.tab_Infinito)
        frame_grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        lbl = ctk.CTkLabel(frame_controles, text="Ingresa función:", font=("Arial", 16))
        lbl.pack(pady=(20, 5), padx=20, anchor="w")
        
       
        self.entry_infinito = ctk.CTkEntry(frame_controles, width=220)
        self.entry_infinito.pack(pady=5, padx=20)
        
        btn = ctk.CTkButton(frame_controles, text="Graficar", command=self.graficar_infinito)
        btn.pack(pady=15, padx=20)
        
        self.fig_inf, self.eje_inf, self.canvas_inf = self.crear_canvas(frame_grafico)

    def graficar_infinito(self):
        print(f"Graficando desde Infinito: {self.entry_infinito.get()}")


#________________________________________TRIGONOMETRICOS__________________________________________________
    def crear_Trigonometricos(self):
        frame_controles = ctk.CTkFrame(self.tab_Trigonometricos, width=300)
        frame_controles.pack(side="left", fill="y", padx=10, pady=10)
        
        frame_grafico = ctk.CTkFrame(self.tab_Trigonometricos)
        frame_grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        lbl = ctk.CTkLabel(frame_controles, text="Ingresa función:", font=("Arial", 16))
        lbl.pack(pady=(20, 5), padx=20, anchor="w")
        
       
        self.entry_trig = ctk.CTkEntry(frame_controles, width=220)
        self.entry_trig.pack(pady=5, padx=20)
        
        btn = ctk.CTkButton(frame_controles, text="Graficar", command=self.graficar_trigonometricos)
        btn.pack(pady=15, padx=20)
        
        self.fig_trig, self.eje_trig, self.canvas_trig = self.crear_canvas(frame_grafico)

    def graficar_trigonometricos(self):
        print(f"Graficando desde Trig: {self.entry_trig.get()}")
        

    def crear_Laterales(self):
        frame_controles = ctk.CTkFrame(self.tab_laterales, width=300)
        frame_controles.pack(side="left", fill="y", padx=10, pady=10)
        
        frame_grafico = ctk.CTkFrame(self.tab_laterales)
        frame_grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        lbl = ctk.CTkLabel(frame_controles, text="Ingresa función:", font=("Arial", 16))
        lbl.pack(pady=(20, 5), padx=20, anchor="w")
        
        self.entry_lat = ctk.CTkEntry(frame_controles, width=220)
        self.entry_lat.pack(pady=5, padx=20)
        
        btn = ctk.CTkButton(frame_controles, text="Graficar", command=self.graficar_laterales)
        btn.pack(pady=15, padx=20)
        
        self.fig_lat, self.eje_lat, self.canvas_lat = self.crear_canvas(frame_grafico)

    def graficar_laterales(self):
        print(f"Graficando desde Laterales: {self.entry_lat.get()}")


    def crear_Tendenciainfinita(self):
        frame_controles = ctk.CTkFrame(self.tab_Tendenciainfinita, width=300)
        frame_controles.pack(side="left", fill="y", padx=10, pady=10)
        
        frame_grafico = ctk.CTkFrame(self.tab_Tendenciainfinita)
        frame_grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        lbl = ctk.CTkLabel(frame_controles, text="Ingresa función:", font=("Arial", 16))
        lbl.pack(pady=(20, 5), padx=20, anchor="w")
        
       
        self.entry_tend = ctk.CTkEntry(frame_controles, width=220)
        self.entry_tend.pack(pady=5, padx=20)
        
        btn = ctk.CTkButton(frame_controles, text="Graficar", command=self.graficar_tendencia)
        btn.pack(pady=15, padx=20)
        
        self.fig_tend, self.eje_tend, self.canvas_tend = self.crear_canvas(frame_grafico)

    def graficar_tendencia(self):
        print(f"Graficando desde Tendencia: {self.entry_tend.get()}")


#______________________________________INFINITOYRADICALES_________________________________________________
    def crear_Infinitoyradicales(self):
        frame_controles = ctk.CTkFrame(self.tab_Infinitoyradicales, width=300)
        frame_controles.pack(side="left", fill="y", padx=10, pady=10)
        
        frame_grafico = ctk.CTkFrame(self.tab_Infinitoyradicales)
        frame_grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        lbl = ctk.CTkLabel(frame_controles, text="Ingresa función:", font=("Arial", 16))
        lbl.pack(pady=(20, 5), padx=20, anchor="w")
       
        self.entry_rad = ctk.CTkEntry(frame_controles, width=220)
        self.entry_rad.pack(pady=5, padx=20)
        
        btn = ctk.CTkButton(frame_controles, text="Graficar", command=self.graficar_radicales)
        btn.pack(pady=15, padx=20)
        
        self.fig_rad, self.eje_rad, self.canvas_rad = self.crear_canvas(frame_grafico)

    def graficar_radicales(self):
        print(f"Graficando desde Radicales: {self.entry_rad.get()}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
