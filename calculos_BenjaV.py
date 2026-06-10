import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

class AppCalculadoraLimites(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.title("Calculadora de límites")
        self.geometry("1200x720")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configuración de columnas
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Contenedores
        self.panel_izquierdo = ctk.CTkFrame(self, width=400, corner_radius=15)
        self.panel_izquierdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.panel_izquierdo.pack_propagate(False)

        self.panel_derecho = ctk.CTkFrame(self, corner_radius=15)
        self.panel_derecho.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Componentes panel izquierdo
        self.titulo = ctk.CTkLabel(self.panel_izquierdo, text="Calculadora de Límites", font=("Arial", 26, "bold"))
        self.titulo.pack(pady=25)

        self.lbl_funcion = ctk.CTkLabel(self.panel_izquierdo, text="Ingrese la función f(x):", font=("Arial", 14))
        self.lbl_funcion.pack(anchor="w", padx=30, pady=5)
        
        self.entrada_funcion = ctk.CTkEntry(self.panel_izquierdo, placeholder_text="Ej: sin(x)/x", width=340)
        self.entrada_funcion.pack(pady=5)

        self.lbl_h = ctk.CTkLabel(self.panel_izquierdo, text="Punto al que tiende x:", font=("Arial", 14))
        self.lbl_h.pack(anchor="w", padx=30, pady=5)
        
        self.entrada_h = ctk.CTkEntry(self.panel_izquierdo, placeholder_text="Ej: 0, inf, pi", width=340)
        self.entrada_h.pack(pady=5)

        self.boton_calcular = ctk.CTkButton(self.panel_izquierdo, text="Calcular y Graficar", command=self.evento_calcular)
        self.boton_calcular.pack(pady=25)

        self.lbl_resultado = ctk.CTkLabel(self.panel_izquierdo, text="Resultado y Análisis:", font=("Arial", 14))
        self.lbl_resultado.pack(anchor="w", padx=30, pady=5)

        self.caja_resultado = ctk.CTkTextbox(self.panel_izquierdo, width=340, height=280, font=("Arial", 13))
        self.caja_resultado.pack(pady=5)
        self.mostrar_texto("Nota: Recuerde usar el asterisco (*) para multiplicar.\nEjemplo: 2*x en lugar de 2x.")

        # Generar el espacio del gráfico
        self.figura, self.ax, self.canvas = self.crear_canvas(self.panel_derecho)

    def crear_canvas(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        eje = figura.add_subplot(111)
        eje.axhline(0, color="black", linewidth=1.2)
        eje.axvline(0, color="black", linewidth=1.2)
        eje.grid(True)
        eje.set_title("Gráfica de la Función")
        
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        canvas.draw()
        return figura, eje, canvas

    def mostrar_texto(self, texto):
        self.caja_resultado.configure(state="normal")
        self.caja_resultado.delete("1.0", "end")
        self.caja_resultado.insert("1.0", texto)
        self.caja_resultado.configure(state="disabled")

    def evento_calcular(self):
        funcion_texto = self.entrada_funcion.get()
        valor_h_texto = self.entrada_h.get()

if __name__ == "__main__":
    app = AppCalculadoraLimites()
    app.mainloop()