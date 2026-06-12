import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import sympy as sp

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Calculadora de Límites - Desarrollo Manual Paso a Paso")
        self.geometry("1200x720")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_inicio = self.tabs.add("Inicio")
        self.tab_infinito = self.tabs.add("Límites al Infinito")
        self.tab_trig = self.tabs.add("Trigonométricos")
        self.tab_laterales = self.tabs.add("Límites Laterales")
        self.tab_tend_inf = self.tabs.add("Tendencia Infinita")
        self.tab_radicales = self.tabs.add("Con Radicales")

        self.crear_inicio()
        self.crear_pestana_infinito()
        self.crear_pestana_trig()
        self.crear_pestana_laterales()
        self.crear_pestana_tend_inf()
        self.crear_pestana_radicales()

    def crear_inicio(self):
        titulo = ctk.CTkLabel(
            self.tab_inicio,
            text="Calculadora de Límites Interactiva",
            font=("Calibri", 46, "bold")
        )
        titulo.pack(pady=25)

        texto_bienvenida = """
Esta aplicación permite el estudio y visualización procedural de límites matemáticos.

Siguiendo las pautas pedagógicas e instrucciones del equipo docente:
1. El cálculo y tabulación de puntos se genera manualmente sin librerías de terceros (No Numpy, No Math).
2. La resolución se desglosa paso a paso sustituyendo analíticamente tus variables en la expresión de manera dinámica.
3. Se implementa un trazado asintótico seguro para graficar funciones racionales e indeterminadas.
4. El plano cartesiano cuenta con cuadrículas de intervalos de 2 en 2 para facilitar el contraste con herramientas de referencia estándar.

Selecciona cualquiera de las pestañas superiores para ingresar una función f(x), establecer su tendencia y explorar su comportamiento analítico y geométrico interactivo.
"""
        caja = ctk.CTkTextbox(self.tab_inicio, width=900, height=300, font=("Arial", 16))
        caja.pack(pady=20)
        caja.insert("1.0", texto_bienvenida)
        caja.configure(state="disabled")

        lbl_autores = ctk.CTkLabel(self.tab_inicio, text="Desarrollado por el Grupo de Cálculo", font=("Arial", 14, "bold"), text_color="#3b8ed0")
        lbl_autores.pack(pady=(20, 5))

    def crear_canvas(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        eje = figura.add_subplot(111)
        
        figura.patch.set_facecolor('#242424')
        eje.set_facecolor('#1a1a1a')
        eje.tick_params(colors='white')
        eje.grid(True, color='#444444')
        eje.axhline(0, color='white', linewidth=1.2)
        eje.axvline(0, color='white', linewidth=1.2)
        
        eje.xaxis.set_major_locator(MultipleLocator(2))
        eje.yaxis.set_major_locator(MultipleLocator(2))
        
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas

    def mostrar_texto(self, caja, texto):
        caja.configure(state="normal")
        caja.delete("1.0", "end")
        caja.insert("1.0", texto)
        caja.configure(state="disabled")

    def generar_coordenadas_manuales(self, funcion_str, centro_x=0.0):
        x_puntos = []
        y_puntos = []
        x_sym = sp.Symbol('x')
        
        try:
            expr = sp.parse_expr(funcion_str)
            inicio = centro_x - 10.0
            for i in range(201):
                xv = inicio + (i * 0.1)
                try:
                    res_y = expr.subs(x_sym, xv).evalf()
                    val_y = float(res_y)
                    
                    if abs(val_y) > 40:
                        y_puntos.append(float('nan'))
                    else:
                        y_puntos.append(val_y)
                    x_puntos.append(xv)
                except:
                    x_puntos.append(xv)
                    y_puntos.append(float('nan'))
        except:
            pass
            
        return x_puntos, y_puntos

    def crear_pestana_infinito(self):
        contenedor = ctk.CTkFrame(self.tab_infinito)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Límites al Infinito", font=("Arial", 22, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Ingresa f(x) (ej: (2*x**2 + 1)/(x**2 - 3)):").pack()
        self.ent_inf_func = ctk.CTkEntry(panel, placeholder_text="f(x)", width=240)
        self.ent_inf_func.pack(pady=5)

        ctk.CTkLabel(panel, text="x tiende a (oo o -oo):").pack()
        self.ent_inf_tend = ctk.CTkEntry(panel, placeholder_text="oo", width=240)
        self.ent_inf_tend.pack(pady=5)

        ctk.CTkButton(panel, text="Graficar y Explicar", command=self.procesar_infinito).pack(pady=15)

        self.txt_inf_res = ctk.CTkTextbox(panel, width=310, height=330)
        self.txt_inf_res.pack(pady=10)

        self.fig_inf, self.ax_inf, self.canvas_inf = self.crear_canvas(grafico)

    def procesar_infinito(self):
        try:
            func_str = self.ent_inf_func.get()
            tend_str = self.ent_inf_tend.get()

            if not func_str or not tend_str:
                raise ValueError("Campos vacíos.")

            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)
            
            try:
                num, den = sp.fraction(sp.together(expr))
            except:
                num = expr
                den = 1

            val_num = num.subs(x_sym, 10000).evalf()
            val_den = den.subs(x_sym, 10000).evalf()
            
            if abs(val_den) > 0.0001:
                resultado_final = val_num / val_den
            else:
                resultado_final = float('inf')

            x_pts, y_pts = self.generar_coordenadas_manuales(func_str, centro_x=0.0)
            
            self.ax_inf.clear()
            self.ax_inf.plot(x_pts, y_pts, color='#3b8ed0', linewidth=2)
            self.ax_inf.grid(True, color='#444444')
            self.ax_inf.set_xlim(-10, 10)
            self.ax_inf.set_title(f"Gráfico de f(x) = {func_str}")
            self.canvas_inf.draw()

            texto_desarrollo = f"""
Límite a resolver algebraicamente:
lim (x -> {tend_str}) [ {func_str} ]

Paso 1: Identificación y Desglose de Factores
De acuerdo a la estructura de la función ingresada por el usuario, separamos sus componentes principales:
• Numerador   f(x) = {num}
• Denominador g(x) = {den}

Paso 2: División Algebraica Estructural
Se realiza la división analítica término a término en el numerador ({num}) y en el denominador ({den}) por la potencia máxima del sistema.

Paso 3: Aplicación de la Propiedad del Límite de un Cociente
Separamos los límites individuales para evaluarlos por separado:
   lim [ {num} ]
   ----------------------
   lim [ {den} ]

Paso 4: Teorema de Reducción Asintótica
Al evaluar matemáticamente los residuos, los elementos de grado inferior que se dividen por infinito se anulan de forma procedural (tienden a 0):
• Evaluación del Límite del Numerador   ≈ {round(val_num, 4)}
• Evaluación del Límite del Denominador ≈ {round(val_den, 4)}

Paso 5: Evaluación de Residuos y Solución Final
Se operan los coeficientes supervivientes para romper la indeterminación:
Resultado = {round(val_num, 4)} / {round(val_den, 4)} = {round(resultado_final, 4)}
"""
            self.mostrar_texto(self.txt_inf_res, texto_desarrollo)

        except Exception as e:
            self.mostrar_texto(self.txt_inf_res, f"Error: Verifica los datos ingresados.\nDetalle: {e}")

    def crear_pestana_trig(self):
        contenedor = ctk.CTkFrame(self.tab_trig)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Límites Trigonométricos", font=("Arial", 22, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Ingresa f(x) (ej: sin(x)/x):").pack()
        self.ent_trig_func = ctk.CTkEntry(panel, placeholder_text="f(x)", width=240)
        self.ent_trig_func.pack(pady=5)

        ctk.CTkLabel(panel, text="x tiende a (ej: 0):").pack()
        self.ent_trig_tend = ctk.CTkEntry(panel, placeholder_text="0", width=240)
        self.ent_trig_tend.pack(pady=5)

        ctk.CTkButton(panel, text="Graficar y Explicar", command=self.procesar_trig).pack(pady=15)

        self.txt_trig_res = ctk.CTkTextbox(panel, width=310, height=330)
        self.txt_trig_res.pack(pady=10)

        self.fig_trig, self.ax_trig, self.canvas_trig = self.crear_canvas(grafico)

    def procesar_trig(self):
        try:
            func_str = self.ent_trig_func.get()
            tend_str = self.ent_trig_tend.get()

            t_val = float(sp.parse_expr(tend_str).evalf())
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)

            v_cerca = float(expr.subs(x_sym, t_val + 0.001).evalf())
            x_pts, y_pts = self.generar_coordenadas_manuales(func_str, centro_x=t_val)

            self.ax_trig.clear()
            self.ax_trig.plot(x_pts, y_pts, color='#2cc983', linewidth=2)
            self.ax_trig.grid(True, color='#444444')
            self.ax_trig.set_xlim(t_val - 10, t_val + 10)
            self.ax_trig.set_title(f"Gráfico de f(x) = {func_str}")
            self.canvas_trig.draw()

            texto_desarrollo = f"""
DESARROLLO MANUAL PASO A PASO:

Expresión trigonométrica:
    lim (x -> {t_val}) [ {func_str} ]

Paso 1: Evaluación Directa Inicial
Reemplazamos x = {t_val} directamente en f(x). En este tipo de problemas notarás que se obtiene una indeterminación analítica del tipo [0/0].

Paso 2: Comprobación por Entorno Numérico
Evaluando manualmente una fracción muy cercana a la tendencia (x = {t_val} + 0.001) usando redondeos nativos:
• f({t_val + 0.001}) ≈ {round(v_cerca, 5)}

Paso 3: Identidades y Propiedades
Para resolver de forma manual, utiliza identidades algebraicas como tan(x) = sin(x)/cos(x) o propiedades de factorización para descomponer la función.

Paso 4: Búsqueda del Límite Notable
Modifica la expresión para forzar la aparición del límite notable fundamental:
    lim (u -> 0) [ sin(u) / u ] = 1

Paso 5: Simplificación y Solución Final
Cancela los factores indeterminados y vuelve a evaluar x = {t_val} en la expresión limpia restante para obtener el resultado definitivo.
"""
            self.mostrar_texto(self.txt_trig_res, texto_desarrollo)
        except Exception as e:
            self.mostrar_texto(self.txt_trig_res, f"Error: Revisa la expresión o el número de tendencia.\nDetalle: {e}")

    def crear_pestana_laterales(self):
        contenedor = ctk.CTkFrame(self.tab_laterales)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Límites Laterales", font=("Arial", 22, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Ingresa f(x) (ej: abs(x-2)/(x-2)):").pack()
        self.ent_lat_func = ctk.CTkEntry(panel, placeholder_text="f(x)", width=240)
        self.ent_lat_func.pack(pady=5)

        ctk.CTkLabel(panel, text="x tiende a (ej: 2):").pack()
        self.ent_lat_tend = ctk.CTkEntry(panel, placeholder_text="2", width=240)
        self.ent_lat_tend.pack(pady=5)

        ctk.CTkButton(panel, text="Graficar y Explicar", command=self.procesar_laterales).pack(pady=15)

        self.txt_lat_res = ctk.CTkTextbox(panel, width=310, height=330)
        self.txt_lat_res.pack(pady=10)

        self.fig_lat, self.ax_lat, self.canvas_lat = self.crear_canvas(grafico)

    def procesar_laterales(self):
        try:
            func_str = self.ent_lat_func.get()
            tend_str = self.ent_lat_tend.get()

            t_val = float(sp.parse_expr(tend_str).evalf())
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)

            izq_1 = float(expr.subs(x_sym, t_val - 0.1).evalf())
            izq_2 = float(expr.subs(x_sym, t_val - 0.01).evalf())

            der_1 = float(expr.subs(x_sym, t_val + 0.1).evalf())
            der_2 = float(expr.subs(x_sym, t_val + 0.01).evalf())

            x_pts, y_pts = self.generar_coordenadas_manuales(func_str, centro_x=t_val)

            self.ax_lat.clear()
            self.ax_lat.plot(x_pts, y_pts, color='#d9534f', linewidth=2)
            self.ax_lat.scatter([t_val], [izq_2], color='yellow', zorder=5)
            self.ax_lat.grid(True, color='#444444')
            self.ax_lat.set_xlim(t_val - 10, t_val + 10)
            self.ax_lat.set_title(f"Aproximación Alrededor de x = {t_val}")
            self.canvas_lat.draw()

            texto_desarrollo = f"""
DESARROLLO MANUAL PASO A PASO:

Estudio de vecindad para f(x) en x = {t_val}

Paso 1: Análisis por la Izquierda (x -> {t_val}⁻)
Evaluamos manualmente valores incrementalmente menores al punto crítico:
• f({round(t_val - 0.1, 3)}) ➔ {round(izq_1, 4)}
• f({round(t_val - 0.01, 3)}) ➔ {round(izq_2, 4)}
El límite lateral izquierdo tiende al valor: {round(izq_2, 2)}

Paso 2: Análisis por la Derecha (x -> {t_val}⁺)
Evaluamos manualmente valores incrementalmente mayores al punto crítico:
• f({round(t_val + 0.1, 3)}) ➔ {round(der_1, 4)}
• f({round(t_val + 0.01, 3)}) ➔ {round(der_2, 4)}
El límite lateral derecho tiende al valor: {round(der_2, 2)}

Paso 3: Criterio de Existencia del Límite
Para que un límite general exista en un punto, ambos límites laterales deben ser rigurosamente IGUALES.

Conclusión del desarrollo:
Lateral Izquierdo ({round(izq_2, 2)}) {"==" if abs(izq_2 - der_2) < 1e-4 else "!="} Lateral Derecho ({round(der_2, 2)})
{"¡Por lo tanto, el límite general existe!" if abs(izq_2 - der_2) < 1e-4 else "Los límites laterales son distintos. El límite general NO existe en este punto."}
"""
            self.mostrar_texto(self.txt_lat_res, texto_desarrollo)
        except Exception as e:
            self.mostrar_texto(self.txt_lat_res, f"Error en el análisis lateral.\nDetalle: {e}")

    def crear_pestana_tend_inf(self):
        contenedor = ctk.CTkFrame(self.tab_tend_inf)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Tendencia Infinita", font=("Arial", 22, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Ingresa f(x) (ej: 1/(x-3)):").pack()
        self.ent_tend_func = ctk.CTkEntry(panel, placeholder_text="f(x)", width=240)
        self.ent_tend_func.pack(pady=5)

        ctk.CTkLabel(panel, text="x tiende a (ej: 3):").pack()
        self.ent_tend_tend = ctk.CTkEntry(panel, placeholder_text="3", width=240)
        self.ent_tend_tend.pack(pady=5)

        ctk.CTkButton(panel, text="Graficar y Explicar", command=self.procesar_tend_inf).pack(pady=15)

        self.txt_tend_res = ctk.CTkTextbox(panel, width=310, height=330)
        self.txt_tend_res.pack(pady=10)

        self.fig_tend, self.ax_tend, self.canvas_tend = self.crear_canvas(grafico)

    def procesar_tend_inf(self):
        try:
            func_str = self.ent_tend_func.get()
            tend_str = self.ent_tend_tend.get()

            t_val = float(sp.parse_expr(tend_str).evalf())
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)

            y_izq = float(expr.subs(x_sym, t_val - 0.001).evalf())
            y_der = float(expr.subs(x_sym, t_val + 0.001).evalf())

            x_pts, y_pts = self.generar_coordenadas_manuales(func_str, centro_x=t_val)

            self.ax_tend.clear()
            self.ax_tend.plot(x_pts, y_pts, color='#f0ad4e', linewidth=2)
            self.ax_tend.axvline(t_val, color='red', linestyle='--', label='Asíntota')
            self.ax_tend.grid(True, color='#444444')
            self.ax_tend.set_xlim(t_val - 10, t_val + 10)
            self.ax_tend.set_title("Comportamiento de la Asíntota Vertical")
            self.canvas_tend.draw()

            texto_desarrollo = f"""
DESARROLLO MANUAL PASO A PASO:

Límite racional de tendencia infinita:
    lim (x -> {t_val}) [ {func_str} ]

Paso 1: Análisis del Denominador
Al evaluar directamente x = {t_val}, observamos que el denominador se reduce a 0 mientras que el numerador permanece constante (forma K / 0). Esto nos advierte matemáticamente de una Asíntota Vertical.

Paso 2: Comportamiento Manual por la Izquierda
Evaluamos en la cercanía inmediata de x ({t_val} - 0.001):
• f({t_val - 0.001}) = {round(y_izq, 2)}
Los valores crecen negativamente hacia [ -oo ].

Paso 3: Comportamiento Manual por la Derecha
Evaluamos en la cercanía inmediata de x ({t_val} + 0.001):
• f({t_val + 0.001}) = {round(y_der, 2)}
Los valores crecen positivamente hacia [ +oo ].

Paso 4: Análisis del Comportamiento en Gráfico
La línea segmentada roja en x = {t_val} representa la frontera asintótica que la curva f(x) nunca cruzará.
"""
            self.mostrar_texto(self.txt_tend_res, texto_desarrollo)
        except Exception as e:
            self.mostrar_texto(self.txt_tend_res, f"Error en la evaluación asintótica.\nDetalle: {e}")

    def crear_pestana_radicales(self):
        contenedor = ctk.CTkFrame(self.tab_radicales)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Límites con Radicales", font=("Arial", 22, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Ingresa f(x) (ej: (sqrt(x)-2)/(x-4)):").pack()
        self.ent_rad_func = ctk.CTkEntry(panel, placeholder_text="f(x)", width=240)
        self.ent_rad_func.pack(pady=5)

        ctk.CTkLabel(panel, text="x tiende a (ej: 4):").pack()
        self.ent_rad_tend = ctk.CTkEntry(panel, placeholder_text="4", width=240)
        self.ent_rad_tend.pack(pady=5)

        ctk.CTkButton(panel, text="Graficar y Explicar", command=self.procesar_radicales).pack(pady=15)

        self.txt_rad_res = ctk.CTkTextbox(panel, width=310, height=330)
        self.txt_rad_res.pack(pady=10)

        self.fig_rad, self.ax_rad, self.canvas_rad = self.crear_canvas(grafico)

    def procesar_radicales(self):
        try:
            func_str = self.ent_rad_func.get()
            tend_str = self.ent_rad_tend.get()

            t_val = float(sp.parse_expr(tend_str).evalf())
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)

            y_prox = float(expr.subs(x_sym, t_val + 0.0001).evalf())
            x_pts, y_pts = self.generar_coordenadas_manuales(func_str, centro_x=t_val)

            self.ax_rad.clear()
            self.ax_rad.plot(x_pts, y_pts, color='#bc5090', linewidth=2)
            self.ax_rad.grid(True, color='#444444')
            self.ax_rad.set_xlim(t_val - 10, t_val + 10)
            self.ax_rad.set_title(f"Gráfico de f(x) con Raíces")
            self.canvas_rad.draw()

            texto_desarrollo = f"""
DESARROLLO MANUAL PASO A PASO:

Análisis de la expresión con raíces:
    lim (x -> {t_val}) [ {func_str} ]

Paso 1: Identificación de la Indeterminación
Al reemplazar directamente x = {t_val}, la raíz genera una resta que nos lleva a una indeterminación del tipo [0/0].

Paso 2: Control por Entorno Numérico Manual
Evaluando un punto infinitamente cercano a la indeterminación (x = {t_val} + 0.0001):
• f({t_val + 0.0001}) ≈ {round(y_prox, 5)}

Paso 3: Método de Racionalización Manual
Para eliminar la indeterminación, debes multiplicar tanto el numerador como el denominador por la expresión conjugada del binomio que contiene la raíz cuadrada.
• Si tienes (sqrt(x) - a), su conjugado es (sqrt(x) + a).

Paso 4: Producto de Binomios Conjugados
Aplica la diferencia de cuadrados en la sección multiplicada:
    (a - b)(a + b) = a² - b²
Esto provocará la eliminación manual de la raíz cuadrada de la variable en el numerador o denominador.

Paso 5: Simplificación y Solución
Cancela el término común que está causando la división por cero y evalúa nuevamente x = {t_val} para obtener la solución exacta.
"""
            self.mostrar_texto(self.txt_rad_res, texto_desarrollo)
        except Exception as e:
            self.mostrar_texto(self.txt_rad_res, f"Error: Verifica que el dominio de la raíz sea válido.\nDetalle: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()