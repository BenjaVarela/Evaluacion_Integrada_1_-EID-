import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import sympy as sp

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Calculadora de Límites")
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
        self.tab_algebraicos = self.tabs.add("Límites Algebraicos")

        self.crear_inicio()
        self.crear_pestana_infinito()
        self.crear_pestana_trig()
        self.crear_pestana_laterales()
        self.crear_pestana_tend_inf()
        self.crear_pestana_radicales()
        self.crear_pestana_algebraicos()

    def crear_inicio(self):
        titulo = ctk.CTkLabel(self.tab_inicio, text="Calculadora de Límites", font=("Calibri", 46, "bold"))
        titulo.pack(pady=25)
        texto_bienvenida = ("Bienvenido al Analizador y Visualizador de Límites.")
        caja = ctk.CTkTextbox(self.tab_inicio, width=900, height=150, font=("Arial", 16))
        caja.pack(pady=20)
        caja.insert("1.0", texto_bienvenida)
        caja.configure(state="disabled")

    def crear_canvas(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        eje = figura.add_subplot(111)
        figura.patch.set_facecolor('#242424')
        eje.set_facecolor('#1a1a1a')
        eje.tick_params(colors='white')
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas

    def configurar_grafico(self, ax, titulo, centro_x=0.0):
        ax.grid(True, color='#444444')
        ax.axhline(0, color='white', linewidth=1.2)
        ax.axvline(0, color='white', linewidth=1.2)
        ax.set_xlim(centro_x - 10, centro_x + 10)
        ax.set_ylim(-10, 10)
        ax.xaxis.set_major_locator(MultipleLocator(2))
        ax.yaxis.set_major_locator(MultipleLocator(2))
        ax.set_title(titulo, color='white')

    def generar_coordenadas(self, funcion_str, centro_x=0.0):
        x_pts, y_pts = [], []
        x_sym = sp.Symbol('x')
        try:
            expr = sp.parse_expr(funcion_str)
            inicio = centro_x - 10.0
            for i in range(201):
                xv = inicio + (i * 0.1)
                try:
                    val_y = float(expr.subs(x_sym, xv).evalf())
                    if abs(val_y) > 40:
                        y_pts.append(float('nan'))
                    else:
                        y_pts.append(val_y)
                    x_pts.append(xv)
                except:
                    x_pts.append(xv)
                    y_pts.append(float('nan'))
        except:
            pass
        return x_pts, y_pts

    def crear_pestana_infinito(self):
        contenedor = ctk.CTkFrame(self.tab_infinito)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)
        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Límites al Infinito", font=("Arial", 22, "bold")).pack(pady=30)
        ctk.CTkLabel(panel, text="Ingresa f(x):").pack()
        self.ent_inf_func = ctk.CTkEntry(panel, width=240)
        self.ent_inf_func.pack(pady=5)
        ctk.CTkLabel(panel, text="x tiende a (oo o -oo):").pack()
        self.ent_inf_tend = ctk.CTkEntry(panel, width=240)
        self.ent_inf_tend.pack(pady=5)
        ctk.CTkButton(panel, text="Calcular", command=self.procesar_infinito).pack(pady=30)
        
        self.lbl_inf_res = ctk.CTkLabel(panel, text="Resultado: -", font=("Arial", 24, "bold"), text_color="#2cc983")
        self.lbl_inf_res.pack(pady=20)
        
        self.fig_inf, self.ax_inf, self.canvas_inf = self.crear_canvas(grafico)

    def procesar_infinito(self):
        try:
            func_str = self.ent_inf_func.get()
            tend_str = self.ent_inf_tend.get()
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)
            
            val_x = 1e10 if tend_str == "oo" else -1e10
            res_num = float(expr.subs(x_sym, val_x).evalf())
            
            if res_num > 1e5: res_exacto = "oo"
            elif res_num < -1e5: res_exacto = "-oo"
            else: res_exacto = str(sp.nsimplify(res_num, rational=True, tolerance=1e-4))

            x_pts, y_pts = self.generar_coordenadas(func_str, 0.0)
            self.ax_inf.clear()
            self.ax_inf.plot(x_pts, y_pts, color='#3b8ed0', linewidth=2)
            self.configurar_grafico(self.ax_inf, f"f(x) = {func_str}")
            self.canvas_inf.draw()

            self.lbl_inf_res.configure(text=f"Resultado: {res_exacto}")
        except Exception:
            self.lbl_inf_res.configure(text="Error matemático")

    def crear_pestana_trig(self):
        contenedor = ctk.CTkFrame(self.tab_trig)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)
        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Límites Trigonométricos", font=("Arial", 22, "bold")).pack(pady=30)
        ctk.CTkLabel(panel, text="Ingresa f(x):").pack()
        self.ent_trig_func = ctk.CTkEntry(panel, width=240)
        self.ent_trig_func.pack(pady=5)
        ctk.CTkLabel(panel, text="x tiende a:").pack()
        self.ent_trig_tend = ctk.CTkEntry(panel, width=240)
        self.ent_trig_tend.pack(pady=5)
        ctk.CTkButton(panel, text="Calcular", command=self.procesar_trig).pack(pady=30)
        
        self.lbl_trig_res = ctk.CTkLabel(panel, text="Resultado: -", font=("Arial", 24, "bold"), text_color="#2cc983")
        self.lbl_trig_res.pack(pady=20)
        
        self.fig_trig, self.ax_trig, self.canvas_trig = self.crear_canvas(grafico)

    def procesar_trig(self):
        try:
            func_str = self.ent_trig_func.get()
            tend_str = self.ent_trig_tend.get()
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)
            t_val = float(sp.parse_expr(tend_str).evalf())
            
            res_num = float(expr.subs(x_sym, t_val + 1e-6).evalf())
            
            if res_num > 1e4: res_exacto = "oo"
            elif res_num < -1e4: res_exacto = "-oo"
            else: res_exacto = str(sp.nsimplify(res_num, rational=True, tolerance=1e-4))

            x_pts, y_pts = self.generar_coordenadas(func_str, t_val)
            self.ax_trig.clear()
            self.ax_trig.plot(x_pts, y_pts, color='#2cc983', linewidth=2)
            self.configurar_grafico(self.ax_trig, f"f(x) = {func_str}", t_val)
            self.canvas_trig.draw()

            self.lbl_trig_res.configure(text=f"Resultado: {res_exacto}")
        except Exception:
            self.lbl_trig_res.configure(text="Error matemático")

    def crear_pestana_laterales(self):
        contenedor = ctk.CTkFrame(self.tab_laterales)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)
        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Límites Laterales", font=("Arial", 22, "bold")).pack(pady=30)
        ctk.CTkLabel(panel, text="Ingresa f(x):").pack()
        self.ent_lat_func = ctk.CTkEntry(panel, width=240)
        self.ent_lat_func.pack(pady=5)
        ctk.CTkLabel(panel, text="Tendencia (ej: 1+ o 1-):").pack()
        self.ent_lat_tend = ctk.CTkEntry(panel, width=240)
        self.ent_lat_tend.pack(pady=5)
        ctk.CTkButton(panel, text="Calcular", command=self.procesar_laterales).pack(pady=30)
        
        self.lbl_lat_res = ctk.CTkLabel(panel, text="Resultado: -", font=("Arial", 20, "bold"), text_color="#2cc983")
        self.lbl_lat_res.pack(pady=20)
        
        self.fig_lat, self.ax_lat, self.canvas_lat = self.crear_canvas(grafico)

    def procesar_laterales(self):
        try:
            func_str = self.ent_lat_func.get()
            tend_str = self.ent_lat_tend.get().strip()
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)

            if tend_str.endswith('+'):
                num_part = tend_str[:-1]
                t_val = float(sp.parse_expr(num_part).evalf())
                res_num = float(expr.subs(x_sym, t_val + 1e-6).evalf())
                tipo = "Por la Derecha (+)"
            elif tend_str.endswith('-'):
                num_part = tend_str[:-1]
                t_val = float(sp.parse_expr(num_part).evalf())
                res_num = float(expr.subs(x_sym, t_val - 1e-6).evalf())
                tipo = "Por la Izquierda (-)"
            else:
                t_val = float(sp.parse_expr(tend_str).evalf())
                res_num = float(expr.subs(x_sym, t_val + 1e-6).evalf())
                tipo = "Por defecto (+)"

            if res_num > 1e4: 
                res_exacto = "oo"
            elif res_num < -1e4: 
                res_exacto = "-oo"
            else: 
                res_exacto = str(sp.nsimplify(res_num, rational=True, tolerance=1e-4))

            x_pts, y_pts = self.generar_coordenadas(func_str, t_val)
            self.ax_lat.clear()
            self.ax_lat.plot(x_pts, y_pts, color='#d9534f', linewidth=2)
            self.configurar_grafico(self.ax_lat, f"f(x) = {func_str}", t_val)
            self.canvas_lat.draw()

            self.lbl_lat_res.configure(text=f"Resultado {tipo}:\n{res_exacto}", text_color="#2cc983")
        except Exception:
            self.lbl_lat_res.configure(text="Error matemático", text_color="#d9534f")

    def crear_pestana_tend_inf(self):
        contenedor = ctk.CTkFrame(self.tab_tend_inf)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)
        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Tendencia Infinita", font=("Arial", 22, "bold")).pack(pady=30)
        ctk.CTkLabel(panel, text="Ingresa f(x):").pack()
        self.ent_tend_func = ctk.CTkEntry(panel, width=240)
        self.ent_tend_func.pack(pady=5)
        ctk.CTkLabel(panel, text="x tiende a:").pack()
        self.ent_tend_tend = ctk.CTkEntry(panel, width=240)
        self.ent_tend_tend.pack(pady=5)
        ctk.CTkButton(panel, text="Calcular", command=self.procesar_tend_inf).pack(pady=30)
        
        self.lbl_tend_res = ctk.CTkLabel(panel, text="Resultado: -", font=("Arial", 20, "bold"), text_color="#2cc983")
        self.lbl_tend_res.pack(pady=20)
        
        self.fig_tend, self.ax_tend, self.canvas_tend = self.crear_canvas(grafico)

    def procesar_tend_inf(self):
        try:
            func_str = self.ent_tend_func.get()
            tend_str = self.ent_tend_tend.get()
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)
            t_val = float(sp.parse_expr(tend_str).evalf())
            
            izq_num = float(expr.subs(x_sym, t_val - 1e-6).evalf())
            der_num = float(expr.subs(x_sym, t_val + 1e-6).evalf())

            lim_izq = "oo" if izq_num > 1e4 else ("-oo" if izq_num < -1e4 else str(sp.nsimplify(izq_num, tolerance=1e-3)))
            lim_der = "oo" if der_num > 1e4 else ("-oo" if der_num < -1e4 else str(sp.nsimplify(der_num, tolerance=1e-3)))

            x_pts, y_pts = self.generar_coordenadas(func_str, t_val)
            self.ax_tend.clear()
            self.ax_tend.plot(x_pts, y_pts, color='#f0ad4e', linewidth=2)
            self.configurar_grafico(self.ax_tend, f"f(x) = {func_str}", t_val)
            self.ax_tend.axvline(t_val, color='red', linestyle='--')
            self.canvas_tend.draw()

            if lim_izq == lim_der:
                self.lbl_tend_res.configure(text=f"Resultado: {lim_izq}")
            else:
                self.lbl_tend_res.configure(text=f"Asíntota Vertical\nIzq: {lim_izq} | Der: {lim_der}")
        except Exception:
            self.lbl_tend_res.configure(text="Error matemático")

    def crear_pestana_radicales(self):
        contenedor = ctk.CTkFrame(self.tab_radicales)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)
        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Con Radicales", font=("Arial", 22, "bold")).pack(pady=30)
        ctk.CTkLabel(panel, text="Ingresa f(x):").pack()
        self.ent_rad_func = ctk.CTkEntry(panel, width=240)
        self.ent_rad_func.pack(pady=5)
        ctk.CTkLabel(panel, text="x tiende a:").pack()
        self.ent_rad_tend = ctk.CTkEntry(panel, width=240)
        self.ent_rad_tend.pack(pady=5)
        ctk.CTkButton(panel, text="Calcular", command=self.procesar_radicales).pack(pady=30)
        
        self.lbl_rad_res = ctk.CTkLabel(panel, text="Resultado: -", font=("Arial", 24, "bold"), text_color="#2cc983")
        self.lbl_rad_res.pack(pady=20)
        
        self.fig_rad, self.ax_rad, self.canvas_rad = self.crear_canvas(grafico)

    def procesar_radicales(self):
        try:
            func_str = self.ent_rad_func.get()
            tend_str = self.ent_rad_tend.get()
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)
            t_val = float(sp.parse_expr(tend_str).evalf())
            
            res_num = float(expr.subs(x_sym, t_val + 1e-6).evalf())
            
            if res_num > 1e4: res_exacto = "oo"
            elif res_num < -1e4: res_exacto = "-oo"
            else: res_exacto = str(sp.nsimplify(res_num, rational=True, tolerance=1e-4))

            x_pts, y_pts = self.generar_coordenadas(func_str, t_val)
            self.ax_rad.clear()
            self.ax_rad.plot(x_pts, y_pts, color='#bc5090', linewidth=2)
            self.configurar_grafico(self.ax_rad, f"f(x) = {func_str}", t_val)
            self.canvas_rad.draw()

            self.lbl_rad_res.configure(text=f"Resultado: {res_exacto}")
        except Exception:
            self.lbl_rad_res.configure(text="Error matemático")

    def crear_pestana_algebraicos(self):
        contenedor = ctk.CTkFrame(self.tab_algebraicos)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)
        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Indeterminaciones 0/0", font=("Arial", 22, "bold")).pack(pady=30)
        ctk.CTkLabel(panel, text="Ingresa f(x):").pack()
        self.ent_alg_func = ctk.CTkEntry(panel, width=240, placeholder_text="(x**3 + x**2 - 5*x + 3)/(x**4 - x**3 - x**2 + x)")
        self.ent_alg_func.pack(pady=5)
        ctk.CTkLabel(panel, text="x tiende a (h):").pack()
        self.ent_alg_tend = ctk.CTkEntry(panel, width=240, placeholder_text="1")
        self.ent_alg_tend.pack(pady=5)
        ctk.CTkButton(panel, text="Calcular", command=self.procesar_algebraicos).pack(pady=30)
        
        self.lbl_alg_res = ctk.CTkLabel(panel, text="Resultado: -", font=("Arial", 24, "bold"), text_color="#2cc983")
        self.lbl_alg_res.pack(pady=20)
        
        self.fig_alg, self.ax_alg, self.canvas_alg = self.crear_canvas(grafico)

    def procesar_algebraicos(self):
        try:
            func_str = self.ent_alg_func.get()
            tend_str = self.ent_alg_tend.get()
            x_sym = sp.Symbol('x')
            expr = sp.parse_expr(func_str)
            t_val = float(sp.parse_expr(tend_str).evalf())
            
            delta = 1e-7
            val_izq = float(expr.subs(x_sym, t_val - delta).evalf())
            val_der = float(expr.subs(x_sym, t_val + delta).evalf())
            
            res_num = (val_izq + val_der) / 2
            
            if res_num > 1e4: 
                res_exacto = "oo"
            elif res_num < -1e4: 
                res_exacto = "-oo"
            else:
                res_exacto = str(sp.nsimplify(res_num, rational=True, tolerance=1e-3))

            x_pts, y_pts = self.generar_coordenadas(func_str, t_val)
            self.ax_alg.clear()
            self.ax_alg.plot(x_pts, y_pts, color='#2cc983', linewidth=2)
            self.configurar_grafico(self.ax_alg, f"f(x) = {func_str}", t_val)
            self.ax_alg.axvline(t_val, color='orange', linestyle=':', alpha=0.6)
            self.canvas_alg.draw()

            self.lbl_alg_res.configure(text=f"Resultado: {res_exacto}")
        except Exception:
            self.lbl_alg_res.configure(text="Error matemático")

if __name__ == "__main__":
    app = App()
    app.mainloop()
