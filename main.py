# ============================================================
# DEMO DE CUSTOMTKINTER + MATPLOTLIB
# Tema: Secciones cónicas
# Autor: Franco Oyarzo Calisto
# ============================================================
#
# Esta aplicación tiene como objetivo enseñar:
# 1. Cómo crear una ventana con CustomTkinter.
# 2. Cómo usar pestañas con CTkTabview.
# 3. Cómo capturar datos ingresados por el usuario.
# 4. Cómo validar entradas numéricas.
# 5. Cómo mostrar procedimientos paso a paso.
# 6. Cómo incrustar gráficos de Matplotlib dentro de CustomTkinter.
#
# Cónicas incluidas:
# - Circunferencia
# - Elipse
# - Parábola
# - Hipérbola
#
# Instalación necesaria:
# pip install customtkinter matplotlib
#
# Considere lo siguiente, esto es solo un EJEMPLO de como utilizar CustomTKinter
# Juegue con el codigo, rompalo, etc, pero entienda como usar todos los conceptos de CTK
# ============================================================

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


# ============================================================
# CLASE PRINCIPAL DE LA APLICACIÓN
# ============================================================
# En CustomTkinter, una aplicación normalmente se construye
# creando una clase que hereda de ctk.CTk.
#
# ctk.CTk funciona como la ventana principal del programa.
# ============================================================

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana.
        self.title("Demo CustomTkinter - Secciones Cónicas")
        self.geometry("1200x720")

        # Apariencia visual de la aplicación.
        ctk.set_appearance_mode("red")
        ctk.set_default_color_theme("blue")

        # Permite que la ventana se adapte al tamaño disponible.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # CTkTabview permite crear pestañas.
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Creación de pestañas.
        self.tab_inicio = self.tabs.add("Inicio")
        self.tab_circunferencia = self.tabs.add("Limites")
        self.tab_elipse = self.tabs.add("Elipse")
        self.tab_parabola = self.tabs.add("Parábola")
        self.tab_hiperbola = self.tabs.add("Hipérbola")

        # Llamamos a los métodos que construyen cada pestaña.
        self.crear_inicio()
        self.crear_circunferencia()
        self.crear_elipse()
        self.crear_parabola()
        self.crear_hiperbola()

    # ========================================================
    # PESTAÑA DE INICIO
    # ========================================================

    def crear_inicio(self):
        titulo = ctk.CTkLabel(
            self.tab_inicio,
            text="Calculadora de Límites",
            font=("Calibri", 50, "bold")
        )
        titulo.pack(pady=25)

        texto = """
Esta aplicación es una base para que estudiantes de primer año aprendan a usar CustomTkinter.

La idea es construir una interfaz parecida a un GeoGebra pequeño, pero más simple.
En este ejemplo se trabajan secciones cónicas: circunferencia, elipse, parábola e hipérbola.

Cada pestaña permite ingresar datos, graficar la figura y ver el procedimiento paso por paso.

La misma estructura puede usarse más adelante para límites:
- ingresar una función
- calcular límite
- graficar la función
- mostrar desarrollo paso a paso
- pedir interpretación al estudiante
"""

        caja = ctk.CTkTextbox(self.tab_inicio, width=900, height=350, font=("Arial", 16))
        caja.pack(pady=20)
        caja.insert("1.0", texto)
        caja.configure(state="disabled")

    # ========================================================
    # FUNCIÓN AUXILIAR PARA CREAR FIGURAS DE MATPLOTLIB
    # ========================================================
    # Esta función evita repetir código.
    # Crea una figura, un eje y un canvas para incrustar
    # el gráfico dentro de un frame de CustomTkinter.
    # ========================================================

    def crear_canvas(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        eje = figura.add_subplot(111)
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas

    # ========================================================
    # CIRCUNFERENCIA
    # ========================================================

    def crear_circunferencia(self):
        contenedor = ctk.CTkFrame(self.tab_circunferencia)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Circunferencia", font=("Arial", 24, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Centro h:").pack()
        self.c_h = ctk.CTkEntry(panel, placeholder_text="Ej: 0")
        self.c_h.pack(pady=5)

        ctk.CTkLabel(panel, text="Centro k:").pack()
        self.c_k = ctk.CTkEntry(panel, placeholder_text="Ej: 0")
        self.c_k.pack(pady=5)

        ctk.CTkLabel(panel, text="Radio r:").pack()
        self.c_r = ctk.CTkEntry(panel, placeholder_text="Ej: 3")
        self.c_r.pack(pady=5)

        ctk.CTkButton(
            panel,
            text="Graficar y explicar",
            command=self.graficar_circunferencia
        ).pack(pady=20)

        self.resultado_circ = ctk.CTkTextbox(panel, width=310, height=350)
        self.resultado_circ.pack(pady=10)

        self.fig_circ, self.ax_circ, self.canvas_circ = self.crear_canvas(grafico)

    def graficar_circunferencia(self):
        try:
            h = float(self.c_h.get())
            k = float(self.c_k.get())
            r = float(self.c_r.get())

            if r <= 0:
                raise ValueError

            x = []
            y = []

            for i in range(361):
                angulo = math.radians(i)
                x.append(h + r * math.cos(angulo))
                y.append(k + r * math.sin(angulo))

            self.ax_circ.clear()
            self.ax_circ.plot(x, y)
            self.ax_circ.scatter([h], [k])
            self.ax_circ.axhline(0)
            self.ax_circ.axvline(0)
            self.ax_circ.grid(True)
            self.ax_circ.axis("equal")
            self.ax_circ.set_title("Circunferencia")
            self.canvas_circ.draw()

            texto = f"""
Ecuación canónica:

(x - h)² + (y - k)² = r²

Datos:

h = {h}
k = {k}
r = {r}

Reemplazo:

(x - {h})² + (y - {k})² = {r}²

Resultado:

(x - {h})² + (y - {k})² = {r ** 2}

Centro:

C({h}, {k})

Radio:

r = {r}

Explicación:

La circunferencia es el conjunto de puntos que están a la misma distancia del centro.
Esa distancia fija corresponde al radio.
"""
            self.mostrar_texto(self.resultado_circ, texto)

        except ValueError:
            self.mostrar_texto(self.resultado_circ, "Error: ingresa números válidos. El radio debe ser mayor que cero.")

    # ========================================================
    # ELIPSE
    # ========================================================

    def crear_elipse(self):
        contenedor = ctk.CTkFrame(self.tab_elipse)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Elipse", font=("Arial", 24, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Centro h:").pack()
        self.e_h = ctk.CTkEntry(panel, placeholder_text="Ej: 0")
        self.e_h.pack(pady=5)

        ctk.CTkLabel(panel, text="Centro k:").pack()
        self.e_k = ctk.CTkEntry(panel, placeholder_text="Ej: 0")
        self.e_k.pack(pady=5)

        ctk.CTkLabel(panel, text="Semieje horizontal a:").pack()
        self.e_a = ctk.CTkEntry(panel, placeholder_text="Ej: 5")
        self.e_a.pack(pady=5)

        ctk.CTkLabel(panel, text="Semieje vertical b:").pack()
        self.e_b = ctk.CTkEntry(panel, placeholder_text="Ej: 3")
        self.e_b.pack(pady=5)

        ctk.CTkButton(panel, text="Graficar y explicar", command=self.graficar_elipse).pack(pady=20)

        self.resultado_elipse = ctk.CTkTextbox(panel, width=310, height=350)
        self.resultado_elipse.pack(pady=10)

        self.fig_elipse, self.ax_elipse, self.canvas_elipse = self.crear_canvas(grafico)

    def graficar_elipse(self):
        try:
            h = float(self.e_h.get())
            k = float(self.e_k.get())
            a = float(self.e_a.get())
            b = float(self.e_b.get())

            if a <= 0 or b <= 0:
                raise ValueError

            x = []
            y = []

            for i in range(361):
                angulo = math.radians(i)
                x.append(h + a * math.cos(angulo))
                y.append(k + b * math.sin(angulo))

            if a >= b:
                orientacion = "horizontal"
                c = math.sqrt(a ** 2 - b ** 2)
                f1 = (h - c, k)
                f2 = (h + c, k)
            else:
                orientacion = "vertical"
                c = math.sqrt(b ** 2 - a ** 2)
                f1 = (h, k - c)
                f2 = (h, k + c)

            self.ax_elipse.clear()
            self.ax_elipse.plot(x, y)
            self.ax_elipse.scatter([h], [k])
            self.ax_elipse.axhline(0)
            self.ax_elipse.axvline(0)
            self.ax_elipse.grid(True)
            self.ax_elipse.axis("equal")
            self.ax_elipse.set_title("Elipse")
            self.canvas_elipse.draw()

            texto = f"""
Ecuación canónica:

(x - h)² / a² + (y - k)² / b² = 1

Datos:

h = {h}
k = {k}
a = {a}
b = {b}

Reemplazo:

(x - {h})² / {a ** 2} + (y - {k})² / {b ** 2} = 1

Centro:

C({h}, {k})

Orientación:

La elipse es {orientacion}.

Cálculo de focos:

c² = eje mayor² - eje menor²
c = {round(c, 3)}

Focos:

F1 = {f1}
F2 = {f2}

Explicación:

La elipse se forma alrededor de un centro.
Si a es mayor que b, se abre más hacia los lados.
Si b es mayor que a, se abre más hacia arriba y abajo.
"""
            self.mostrar_texto(self.resultado_elipse, texto)

        except ValueError:
            self.mostrar_texto(self.resultado_elipse, "Error: ingresa números válidos. Los semiejes deben ser mayores que cero.")

    # ========================================================
    # PARÁBOLA
    # ========================================================

    def crear_parabola(self):
        contenedor = ctk.CTkFrame(self.tab_parabola)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Parábola", font=("Arial", 24, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Vértice h:").pack()
        self.p_h = ctk.CTkEntry(panel, placeholder_text="Ej: 0")
        self.p_h.pack(pady=5)

        ctk.CTkLabel(panel, text="Vértice k:").pack()
        self.p_k = ctk.CTkEntry(panel, placeholder_text="Ej: 0")
        self.p_k.pack(pady=5)

        ctk.CTkLabel(panel, text="Parámetro p:").pack()
        self.p_p = ctk.CTkEntry(panel, placeholder_text="Ej: 2")
        self.p_p.pack(pady=5)

        self.orientacion_parabola = ctk.CTkOptionMenu(
            panel,
            values=["Vertical", "Horizontal"]
        )
        self.orientacion_parabola.pack(pady=10)

        ctk.CTkButton(panel, text="Graficar y explicar", command=self.graficar_parabola).pack(pady=20)

        self.resultado_parabola = ctk.CTkTextbox(panel, width=310, height=350)
        self.resultado_parabola.pack(pady=10)

        self.fig_parabola, self.ax_parabola, self.canvas_parabola = self.crear_canvas(grafico)

    def graficar_parabola(self):
        try:
            h = float(self.p_h.get())
            k = float(self.p_k.get())
            p = float(self.p_p.get())

            if p == 0:
                raise ValueError

            orientacion = self.orientacion_parabola.get()

            x = []
            y = []

            valores = [i / 10 for i in range(-100, 101)]

            if orientacion == "Vertical":
                for t in valores:
                    x_val = h + t
                    y_val = k + (t ** 2) / (4 * p)
                    x.append(x_val)
                    y.append(y_val)

                foco = (h, k + p)
                directriz = f"y = {k - p}"
                ecuacion = f"(x - {h})² = {4 * p}(y - {k})"

            else:
                for t in valores:
                    y_val = k + t
                    x_val = h + (t ** 2) / (4 * p)
                    x.append(x_val)
                    y.append(y_val)

                foco = (h + p, k)
                directriz = f"x = {h - p}"
                ecuacion = f"(y - {k})² = {4 * p}(x - {h})"

            self.ax_parabola.clear()
            self.ax_parabola.plot(x, y)
            self.ax_parabola.scatter([h], [k])
            self.ax_parabola.axhline(0)
            self.ax_parabola.axvline(0)
            self.ax_parabola.grid(True)
            self.ax_parabola.axis("equal")
            self.ax_parabola.set_title("Parábola")
            self.canvas_parabola.draw()

            texto = f"""
Ecuación canónica de la parábola:

Vertical:
(x - h)² = 4p(y - k)

Horizontal:
(y - k)² = 4p(x - h)

Datos:

h = {h}
k = {k}
p = {p}

Orientación seleccionada:

{orientacion}

Reemplazo:

{ecuacion}

Vértice:

V({h}, {k})

Foco:

F = {foco}

Directriz:

{directriz}

Explicación:

El valor p indica la distancia desde el vértice al foco.
Si p es positivo, la parábola abre hacia arriba o hacia la derecha.
Si p es negativo, abre hacia abajo o hacia la izquierda.
"""
            self.mostrar_texto(self.resultado_parabola, texto)

        except ValueError:
            self.mostrar_texto(self.resultado_parabola, "Error: ingresa números válidos. El parámetro p no puede ser cero.")

    # ========================================================
    # HIPÉRBOLA
    # ========================================================

    def crear_hiperbola(self):
        contenedor = ctk.CTkFrame(self.tab_hiperbola)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Hipérbola", font=("Arial", 24, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Centro h:").pack()
        self.h_h = ctk.CTkEntry(panel, placeholder_text="Ej: 0")
        self.h_h.pack(pady=5)

        ctk.CTkLabel(panel, text="Centro k:").pack()
        self.h_k = ctk.CTkEntry(panel, placeholder_text="Ej: 0")
        self.h_k.pack(pady=5)

        ctk.CTkLabel(panel, text="Semieje a:").pack()
        self.h_a = ctk.CTkEntry(panel, placeholder_text="Ej: 3")
        self.h_a.pack(pady=5)

        ctk.CTkLabel(panel, text="Semieje b:").pack()
        self.h_b = ctk.CTkEntry(panel, placeholder_text="Ej: 2")
        self.h_b.pack(pady=5)

        self.orientacion_hiperbola = ctk.CTkOptionMenu(
            panel,
            values=["Horizontal", "Vertical"]
        )
        self.orientacion_hiperbola.pack(pady=10)

        ctk.CTkButton(panel, text="Graficar y explicar", command=self.graficar_hiperbola).pack(pady=20)

        self.resultado_hiperbola = ctk.CTkTextbox(panel, width=310, height=350)
        self.resultado_hiperbola.pack(pady=10)

        self.fig_hiperbola, self.ax_hiperbola, self.canvas_hiperbola = self.crear_canvas(grafico)

    def graficar_hiperbola(self):
        try:
            h = float(self.h_h.get())
            k = float(self.h_k.get())
            a = float(self.h_a.get())
            b = float(self.h_b.get())

            if a <= 0 or b <= 0:
                raise ValueError

            orientacion = self.orientacion_hiperbola.get()

            x1 = []
            y1 = []
            x2 = []
            y2 = []

            valores = [i / 10 for i in range(-80, 81)]

            if orientacion == "Horizontal":
                for t in valores:
                    x_der = h + a * math.cosh(t)
                    y_der = k + b * math.sinh(t)
                    x_izq = h - a * math.cosh(t)
                    y_izq = k + b * math.sinh(t)

                    x1.append(x_der)
                    y1.append(y_der)
                    x2.append(x_izq)
                    y2.append(y_izq)

                c = math.sqrt(a ** 2 + b ** 2)
                f1 = (h - c, k)
                f2 = (h + c, k)
                ecuacion = f"(x - {h})² / {a ** 2} - (y - {k})² / {b ** 2} = 1"

            else:
                for t in valores:
                    x_sup = h + b * math.sinh(t)
                    y_sup = k + a * math.cosh(t)
                    x_inf = h + b * math.sinh(t)
                    y_inf = k - a * math.cosh(t)

                    x1.append(x_sup)
                    y1.append(y_sup)
                    x2.append(x_inf)
                    y2.append(y_inf)

                c = math.sqrt(a ** 2 + b ** 2)
                f1 = (h, k - c)
                f2 = (h, k + c)
                ecuacion = f"(y - {k})² / {a ** 2} - (x - {h})² / {b ** 2} = 1"

            self.ax_hiperbola.clear()
            self.ax_hiperbola.plot(x1, y1)
            self.ax_hiperbola.plot(x2, y2)
            self.ax_hiperbola.scatter([h], [k])
            self.ax_hiperbola.axhline(0)
            self.ax_hiperbola.axvline(0)
            self.ax_hiperbola.grid(True)
            self.ax_hiperbola.axis("equal")
            self.ax_hiperbola.set_title("Hipérbola")
            self.canvas_hiperbola.draw()

            texto = f"""
Ecuación canónica de la hipérbola:

Horizontal:
(x - h)² / a² - (y - k)² / b² = 1

Vertical:
(y - k)² / a² - (x - h)² / b² = 1

Datos:

h = {h}
k = {k}
a = {a}
b = {b}

Orientación seleccionada:

{orientacion}

Reemplazo:

{ecuacion}

Centro:

C({h}, {k})

Cálculo de focos:

c² = a² + b²
c = {round(c, 3)}

Focos:

F1 = {f1}
F2 = {f2}

Explicación:

La hipérbola tiene dos ramas.
Si es horizontal, las ramas se abren hacia izquierda y derecha.
Si es vertical, las ramas se abren hacia arriba y abajo.
"""
            self.mostrar_texto(self.resultado_hiperbola, texto)

        except ValueError:
            self.mostrar_texto(self.resultado_hiperbola, "Error: ingresa números válidos. a y b deben ser mayores que cero.")

    # ========================================================
    # FUNCIÓN AUXILIAR PARA MOSTRAR TEXTO
    # ========================================================

    def mostrar_texto(self, caja, texto):
        caja.configure(state="normal")
        caja.delete("1.0", "end")
        caja.insert("1.0", texto)
        caja.configure(state="disabled")


# ============================================================
# EJECUCIÓN DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    app = App()
    app.mainloop()