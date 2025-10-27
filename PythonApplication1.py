import tkinter as tk
from tkinter import font
import random
from PIL import Image, ImageTk

# --- 1. Definición de Elementos del Juego ---
PERSONAJES = ["valentina", "marco", "elisa", "lucia", "andres"]
LOCACIONES = ["cubierta", "capitan", "restaurante", "maquinas", "bar"]
ARMAS = ["ancla", "cuchillo", "extintor", "cuerda", "jeringa"]

# 5 Casos de Finales Prediseñados (Culpable, Locación, Arma)
FINALES = [
    ("valentina", "cubierta", "ancla"), # Caso 1: Valentina / Cubierta / Ancla
    ("marco", "maquinas", "cuerda"),    # Caso 2: Marco / Máquinas / Cuerda
    ("elisa", "capitan", "jeringa"),    # Caso 3: Elisa / Camarote del Capitán / Jeringa
    ("lucia", "restaurante", "cuchillo"),# Caso 4: Lucía / Restaurante / Cuchillo
    ("andres", "bar", "extintor")       # Caso 5: Andrés / Bar / Extintor
]

TITULOS = {
    "valentina": "Capitana Valentina", "marco": "Músico Marco", "elisa": "Médica Elisa", 
    "lucia": "Chef Lucía", "andres": "Oficial Andrés", "cubierta": "Cubierta Principal",
    "capitan": "Camarote del Capitán", "restaurante": "Restaurante Mar Azul",
    "maquinas": "Sala de Máquinas", "bar": "Bar Panorámico", "ancla": "Ancla Decorativa",
    "cuchillo": "Cuchillo de Cocina", "extintor": "Extintor Metálico", 
    "cuerda": "Cuerda de Amarre", "jeringa": "Jeringa Desconocida"
}

class CruceroAlAcecho(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crucero al Acecho: Un Misterio a Bordo")
        self.geometry("1280x720")
        self.resizable(False, False)

        # Inicialización de variables
        self.escenario_actual = 0
        self.pistas = {"culpable": [], "locacion": [], "arma": []}
        self.imagenes = {}
        
        self.cargar_imagenes()

        # Estructura principal de la interfaz
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.info_frame = self._crear_info_frame()
        self.pista_label = self._crear_pista_label()

        self.reiniciar_juego()

    def _crear_info_frame(self):
        """Crea el marco principal para el texto de la historia y las opciones (fondo negro)."""
        frame = tk.Frame(self, bg='black', bd=5, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.7, relheight=0.8)
        return frame

    def _crear_pista_label(self):
        """Crea la etiqueta dinámica para mostrar las pistas recientes."""
        label = tk.Label(self, text="Pista: Ninguna todavía.", font=("Arial", 12), fg="#D4AC0D", bg="#1C2833", anchor="w")
        label.place(relx=0.02, rely=0.02, relwidth=0.96, height=30)
        return label

    def cargar_imagenes(self):
        """Carga y almacena todas las imágenes."""
        elementos = PERSONAJES + LOCACIONES + ARMAS
        for nombre in elementos:
            try:
                ruta = f"recursos/{nombre}.jpg"
                img = Image.open(ruta)
                self.imagenes[nombre] = img
            except FileNotFoundError:
                print(f"Error: Imagen {nombre}.jpg no encontrada en la carpeta 'recursos'.")
            except Exception as e:
                print(f"Error al cargar la imagen {nombre}.jpg: {e}")

    def _set_background(self, nombre_imagen, rel_width=1.0, rel_height=1.0, anchor=tk.CENTER, relx=0.5, rely=0.5):
        """Establece la imagen de fondo principal."""
        if nombre_imagen in self.imagenes:
            img_pil = self.imagenes[nombre_imagen]
            
            if rel_width == 1.0 and rel_height == 1.0:
                resized_img = img_pil.resize((self.winfo_width(), self.winfo_height()))
            else:
                width = int(self.winfo_width() * rel_width)
                height = int(self.winfo_height() * rel_height)
                resized_img = img_pil.resize((width, height))
            
            self.tk_image = ImageTk.PhotoImage(resized_img)
            self.bg_label.config(image=self.tk_image)
            self.bg_label.image = self.tk_image
            self.bg_label.place(relx=relx, rely=rely, relwidth=rel_width, relheight=rel_height, anchor=anchor)
        else:
            self.bg_label.config(image='', bg="#1C2833")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def limpiar_frame(self):
        """Elimina todos los widgets del marco de información y asegura fondo negro."""
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        self.info_frame.config(bg='black')
        # Desvincula la tecla Enter de cualquier función anterior
        self.unbind('<Return>') 

    def mostrar_bienvenida(self):
        """Pantalla de bienvenida e introducción a la historia."""
        self._set_background('cubierta')
        self.limpiar_frame()
        self.pista_label.config(text="")

        tk.Label(self.info_frame, text="🚢 CRUCERO AL ACECHO 🕵️‍", font=("Arial", 40, "bold"), fg="#D4AC0D", bg="black").pack(pady=30)

        historia = (
            "La opulencia del crucero 'El Leviatán' ha sido empañada por un crimen atroz. \n"
            "El magnate de las finanzas, el Sr. Thorne, ha sido encontrado sin vida. \n"
            "Todos a bordo son sospechosos. Es su deber, como detective, descubrir: \n"
            "\n"
            "**¿Quién lo hizo? ¿Dónde? ¿Y con qué arma?**\n"
        )
        tk.Label(self.info_frame, text=historia, font=("Arial", 18), fg="#F4F6F6", bg="black", justify=tk.CENTER).pack(pady=20)

        tk.Button(self.info_frame, text="INICIAR INVESTIGACIÓN", command=self.avanzar_escenario, font=("Arial", 20, "bold"), bg="#1A5276", fg="white", padx=20, pady=10).pack(pady=40)

    def avanzar_escenario(self):
        """Avanza al siguiente escenario o al final del juego."""
        self.escenario_actual += 1
        if self.escenario_actual <= 5:
            self.mostrar_escenario()
        else:
            self.mostrar_acusacion_final()

    def mostrar_escenario(self):
        """Muestra la interfaz del escenario con la imagen y las opciones de decisión."""
        
        escenarios_data = {
            1: {"titulo": "Escenario 1: El Rastrillo en la Cubierta", "texto": "Estás en la cubierta. Un tripulante escuchó una discusión. ¿Qué haces?", "locacion_img": "cubierta",
                "opciones": [("Preguntar a Marco sobre ruidos.", self.manejar_decision, ("marco", "ruido")), ("Revisar la zona en busca de objetos o armas fuera de lugar.", self.manejar_decision, ("cubierta", "revision"))]},
            2: {"titulo": "Escenario 2: La Médica y el Silencio", "texto": "Visitas a Elisa. Su actitud es sospechosa, parece saber algo del estado de la Víctima. ¿Cómo la enfrentas?", "locacion_img": "capitan", 
                "opciones": [("Preguntarle sobre la salud de la Víctima y sus disputas.", self.manejar_decision, ("elisa", "disputa")), ("Pedirle análisis forense rápido, buscando toxinas.", self.manejar_decision, ("elisa", "toxinas"))]},
            3: {"titulo": "Escenario 3: La Presión de la Cocina", "texto": "Lucía está nerviosa, y su área es un arsenal potencial. Necesitas saber si su temperamento la traicionó. ¿Qué harás?", "locacion_img": "restaurante",
                "opciones": [("Presionar sobre su historial de temperamento y las cámaras.", self.manejar_decision, ("lucia", "temperamento")), ("Inspeccionar su juego de cuchillos.", self.manejar_decision, ("lucia", "cuchillos"))]},
            4: {"titulo": "Escenario 4: Patrullaje y Registros", "texto": "Andrés controlaba la Sala de Máquinas. Tienes que saber qué vio o qué estaba ocultando.", "locacion_img": "maquinas",
                "opciones": [("Preguntar a Andrés sobre su patrullaje y los equipos de seguridad (extintores, cuerdas).", self.manejar_decision, ("andres", "patrullaje")), ("Buscar objetos perdidos de la Víctima en la zona.", self.manejar_decision, ("maquinas", "objetos"))]},
            5: {"titulo": "Escenario 5: El Motivo Secreto", "texto": "El Bar Panorámico es el último lugar. Última oportunidad para un dato crucial de Valentina sobre la Víctima. ¿A quién confrontas?", "locacion_img": "bar",
                "opciones": [("Confrontar a Valentina con el 'incidente del pasado'.", self.manejar_decision, ("valentina", "confrontar")), ("Interrogar a Marco sobre las deudas y la relación de la Víctima con ellas.", self.manejar_decision, ("marco", "deudas"))]}
        }
        
        data = escenarios_data[self.escenario_actual]
        self._set_background(data["locacion_img"])
        self.limpiar_frame()
        
        tk.Label(self.info_frame, text=data["titulo"], font=("Arial", 28, "bold"), fg="#D4AC0D", bg="black").pack(pady=20)
        tk.Label(self.info_frame, text=data["texto"], font=("Arial", 16), fg="white", bg="black", justify=tk.CENTER, wraplength=700).pack(pady=20)

        opciones_frame = tk.Frame(self.info_frame, bg="black")
        opciones_frame.pack(pady=30)
        
        for texto, comando, args in data["opciones"]:
            tk.Button(opciones_frame, text=texto, command=lambda c=comando, a=args: c(a[0], a[1]), font=("Arial", 14), bg="#34495E", fg="white", padx=15, pady=8, wraplength=600).pack(pady=10)

    def manejar_decision(self, sujeto, tipo_pista):
        """Procesa la decisión del jugador y actualiza las pistas."""
        
        pista_texto = ""
        
        # --- Lógica de Pistas ---
        if self.escenario_actual == 1:
            if sujeto == "marco":
                pista_texto = "Marco confiesa que Valentina y Andrés discutieron en la cubierta antes del crimen. Sospecha sobre ellos."
                self.pistas["culpable"].extend(["valentina", "andres"])
            elif sujeto == "cubierta":
                pista_texto = "Encuentras rastros de arrastre. Un objeto grande o pesado (Ancla/Extintor) pudo ser usado aquí."
                self.pistas["arma"].extend(["ancla", "extintor"])

        elif self.escenario_actual == 2:
            if tipo_pista == "disputa":
                pista_texto = "Elisa confirma que la Víctima peleó con Lucía y Marco por negocios. Refuerza sospecha sobre ellos."
                self.pistas["culpable"].extend(["lucia", "marco"])
            elif tipo_pista == "toxinas":
                if self.arma == "jeringa":
                    pista_texto = "El análisis preliminar detecta una sustancia inusual. ¡La Jeringa es muy probable!"
                    self.pistas["arma"].append("jeringa")
                else:
                    pista_texto = "No hay toxinas, lo que descarta la Jeringa. (Probablemente)"

        elif self.escenario_actual == 3:
            if tipo_pista == "temperamento":
                pista_texto = "Lucía, molesta, dice haber visto a Andrés en un área prohibida. Sospecha sobre la locación y Andrés."
                self.pistas["culpable"].append("andres")
            elif tipo_pista == "cuchillos":
                if self.arma == "cuchillo":
                    pista_texto = "Un cuchillo de alta cocina parece haber sido limpiado de forma apresurada. ¡El Cuchillo es el arma!"
                    self.pistas["arma"].append("cuchillo")
                else:
                    pista_texto = "Todos los cuchillos están en orden, se descarta el Cuchillo."

        elif self.escenario_actual == 4:
            if tipo_pista == "patrullaje":
                pista_texto = "Andrés confirma revisar Extintores y Cuerdas esa noche. Ambos son posibles armas."
                self.pistas["arma"].extend(["extintor", "cuerda"])
            elif tipo_pista == "objetos":
                if self.locacion == "maquinas":
                    pista_texto = "Encuentras un cigarrillo de la Víctima. Estuvo en la Sala de Máquinas."
                    self.pistas["locacion"].append("maquinas")
                else:
                    pista_texto = "El lugar está muy limpio, pero Andrés parece inquieto. No hay pistas físicas de locación."

        elif self.escenario_actual == 5:
            if sujeto == "valentina":
                if self.culpable == "valentina":
                    pista_texto = "Valentina se quiebra: el pasado de Thorne la estaba arruinando. ¡Ella tenía el motivo más fuerte!"
                    self.pistas["culpable"].append("valentina")
                else:
                    pista_texto = "Valentina desvía la conversación a Marco y sus deudas. Sospecha en Marco."
                    self.pistas["culpable"].append("marco")
            elif sujeto == "marco":
                if self.culpable == "marco":
                    pista_texto = "Marco se quiebra, las deudas lo tenían al límite, Thorne era la causa. ¡Sospecha fuerte en Marco!"
                    self.pistas["culpable"].append("marco")
                else:
                    pista_texto = "Marco te da una pista falsa sobre Lucía y su temperamento explosivo. No obtienes pista clara."
        
        self.pista_label.config(text=f"Pista {self.escenario_actual}: {pista_texto}", fg="white")
        self.avanzar_escenario()

    def mostrar_acusacion_final(self):
        """Pantalla de acusación final (Escenario 6)."""
        self._set_background('bar')
        self.limpiar_frame()
        self.pista_label.config(text="📢 HAZ TU ACUSACIÓN FINAL")

        tk.Label(self.info_frame, text="✅ ACUSACIÓN FINAL ✅", font=("Arial", 30, "bold"), fg="#D4AC0D", bg="black").pack(pady=20)
        tk.Label(self.info_frame, text="Ha llegado el momento de la verdad. Selecciona tu sospechoso, locación y arma.", font=("Arial", 16), fg="white", bg="black", justify=tk.CENTER, wraplength=700).pack(pady=10)

        self.var_culpable = tk.StringVar(self)
        self.var_locacion = tk.StringVar(self)
        self.var_arma = tk.StringVar(self)

        self.var_culpable.set("Culpable")
        self.var_locacion.set("Locación")
        self.var_arma.set("Arma")
        
        opciones_frame = tk.Frame(self.info_frame, bg="black")
        opciones_frame.pack(pady=20)

        menu_font = font.Font(family="Arial", size=14)
        
        c_menu = tk.OptionMenu(opciones_frame, self.var_culpable, *[p.capitalize() for p in PERSONAJES])
        c_menu.config(font=menu_font, bg="#34495E", fg="white")
        c_menu["menu"].config(font=menu_font, bg="#34495E", fg="white")
        c_menu.pack(side=tk.LEFT, padx=10)
        
        l_menu = tk.OptionMenu(opciones_frame, self.var_locacion, *[TITULOS[l] for l in LOCACIONES])
        l_menu.config(font=menu_font, bg="#34495E", fg="white")
        l_menu["menu"].config(font=menu_font, bg="#34495E", fg="white")
        l_menu.pack(side=tk.LEFT, padx=10)
        
        a_menu = tk.OptionMenu(opciones_frame, self.var_arma, *[TITULOS[a] for a in ARMAS])
        a_menu.config(font=menu_font, bg="#34495E", fg="white")
        a_menu["menu"].config(font=menu_font, bg="#34495E", fg="white")
        a_menu.pack(side=tk.LEFT, padx=10)

        tk.Button(self.info_frame, text="ACUSAR", command=self.resolver_misterio, font=("Arial", 18, "bold"), bg="#C0392B", fg="white", padx=20, pady=10).pack(pady=30)
        
        tk.Label(self.info_frame, text="Tus Pistas Recolectadas", font=("Arial", 14, "bold"), fg="#D4AC0D", bg="black").pack(pady=(10, 0))
        pistas_recolectadas = (
            f"Sospechosos mencionados: {', '.join([TITULOS[p] for p in set(self.pistas['culpable'])]) if self.pistas['culpable'] else 'Ninguno'}\n"
            f"Locaciones mencionadas: {', '.join([TITULOS[l] for l in set(self.pistas['locacion'])]) if self.pistas['locacion'] else 'Ninguna'}\n"
            f"Armas mencionadas: {', '.join([TITULOS[a] for a in set(self.pistas['arma'])]) if self.pistas['arma'] else 'Ninguna'}"
        )
        tk.Label(self.info_frame, text=pistas_recolectadas, font=("Arial", 12), fg="white", bg="black", justify=tk.LEFT, wraplength=700).pack()

    def _normalize_name(self, name):
        """Convierte los nombres de la interfaz a claves internas (minúsculas)."""
        for key, value in TITULOS.items():
            if name.lower() == key or name.lower() == value.lower():
                return key
        return name.lower()

    def resolver_misterio(self):
        """Compara la acusación del jugador con la solución real."""
        acusacion_culpable = self._normalize_name(self.var_culpable.get())
        acusacion_locacion = self._normalize_name(self.var_locacion.get())
        acusacion_arma = self._normalize_name(self.var_arma.get())
        
        if acusacion_culpable == "culpable" or acusacion_locacion == "locación" or acusacion_arma == "arma":
            self.pista_label.config(text="🚨 ¡ERROR! Debe seleccionar las 3 categorías para acusar.", fg="red")
            return

        self.mostrar_desglose_final(acusacion_culpable, acusacion_locacion, acusacion_arma)

    def mostrar_desglose_final(self, ac_culpable, ac_locacion, ac_arma):
        """Muestra el desglose de aciertos/errores, las imágenes y el botón de continuar."""
        self._set_background('cubierta')
        self.limpiar_frame()

        # Vincula la tecla Enter a la función de opciones finales
        self.bind('<Return>', lambda event: self.mostrar_opciones_finales())
        self.pista_label.config(text="Presiona ENTER para continuar el viaje... ($\hookleftarrow$)", fg="#00FF00")

        acierto_culpable = ac_culpable == self.culpable
        acierto_locacion = ac_locacion == self.locacion
        acierto_arma = ac_arma == self.arma
        acierto_total = acierto_culpable and acierto_locacion and acierto_arma

        if acierto_total:
            titulo = "🎉 ¡VEREDICTO: ACERTASTE EN TODO! 🎉"
            color_titulo = "green"
        else:
            titulo = "❌ ¡VEREDICTO: FALLASTE LA ACUSACIÓN! ❌"
            color_titulo = "red"

        tk.Label(self.info_frame, text=titulo, font=("Arial", 30, "bold"), fg=color_titulo, bg="black").pack(pady=(10, 5))
        
        # --- Desglose de Aciertos/Errores (Se mantiene la estructura) ---
        desglose_frame = tk.Frame(self.info_frame, bg="black")
        desglose_frame.pack(pady=5)

        items_a_revisar = [
            ("Culpable", ac_culpable, self.culpable, acierto_culpable),
            ("Locación", ac_locacion, self.locacion, acierto_locacion),
            ("Arma", ac_arma, self.arma, acierto_arma)
        ]

        for i, (categoria, intento, correcto, acierto) in enumerate(items_a_revisar):
            icon = "✅" if acierto else "❌"
            color = "green" if acierto else "red"

            intento_display = TITULOS.get(intento, intento.capitalize())
            
            tk.Label(desglose_frame, text=f"{icon} {categoria}:", font=("Arial", 14, "bold"), fg=color, bg="black").grid(row=i, column=0, sticky="w", padx=10, pady=3)
            tk.Label(desglose_frame, text=f"Tu Intento: {intento_display}", font=("Arial", 12), fg="white", bg="black").grid(row=i, column=1, sticky="w", pady=3)
            
            if not acierto:
                correcto_display = TITULOS.get(correcto, correcto.capitalize())
                tk.Label(desglose_frame, text=f" | La Solución Era: {correcto_display}", font=("Arial", 12, "italic"), fg="#D4AC0D", bg="black").grid(row=i, column=2, sticky="w", pady=3)
            else:
                tk.Label(desglose_frame, text=" | ¡Acertaste!", font=("Arial", 12, "italic"), fg="#D4AC0D", bg="black").grid(row=i, column=2, sticky="w", pady=3)

        tk.Label(self.info_frame, text="LA VERDAD REVELADA:", font=("Arial", 18, "bold"), fg="#D4AC0D", bg="black").pack(pady=(15, 5))
        
        # --- Visual de la Solución Correcta ---
        solucion_frame = tk.Frame(self.info_frame, bg="black")
        solucion_frame.pack()

        # Usamos imágenes más pequeñas para evitar desbordamiento vertical
        self._mostrar_imagen_secundaria(solucion_frame, self.culpable, 200, 250, row=0, col=0)
        self._mostrar_imagen_secundaria(solucion_frame, self.locacion, 200, 250, row=0, col=1)
        self._mostrar_imagen_secundaria(solucion_frame, self.arma, 120, 120, row=0, col=2, is_square=True)


        # **BOTÓN DE CONTINUAR (Opción de ratón)**
        tk.Button(self.info_frame, text="CONTINUAR", command=self.mostrar_opciones_finales, font=("Arial", 16, "bold"), bg="#1A5276", fg="white", padx=20, pady=10).pack(pady=15)
    
    def _mostrar_imagen_secundaria(self, parent, nombre_imagen, width, height, row, col, is_square=False):
        """Muestra una imagen pequeña en un marco específico."""
        if nombre_imagen in self.imagenes:
            img_pil = self.imagenes[nombre_imagen]
            
            if is_square:
                min_dim = min(img_pil.size)
                img_pil = img_pil.crop((0, 0, min_dim, min_dim))
            
            resized_img = img_pil.resize((width, height))
            tk_image = ImageTk.PhotoImage(resized_img)

            img_label = tk.Label(parent, image=tk_image, text=TITULOS.get(nombre_imagen, nombre_imagen.capitalize()), compound="top", bg="black", fg="#D4AC0D", font=("Arial", 12, "bold"))
            img_label.image = tk_image
            img_label.grid(row=row, column=col, padx=15)
            
        else:
            tk.Label(parent, text=f"Imagen no disponible: {nombre_imagen}", bg="black", fg="white").grid(row=row, column=col, padx=15)

    def mostrar_opciones_finales(self):
        """Muestra la pantalla final para Jugar de Nuevo o Salir."""
        self.unbind('<Return>') # Desvincula Enter para esta pantalla
        self._set_background('cubierta')
        self.limpiar_frame()
        self.pista_label.config(text="")

        tk.Label(self.info_frame, text="¿FIN DEL VIAJE? 🚢", font=("Arial", 30, "bold"), fg="#D4AC0D", bg="black").pack(pady=50)
        tk.Label(self.info_frame, text="El misterio ha sido resuelto (o el asesino ha escapado). ¿Qué deseas hacer ahora?", font=("Arial", 16), fg="white", bg="black").pack(pady=20)

        btn_frame = tk.Frame(self.info_frame, bg="black")
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="JUGAR DE NUEVO", command=self.reiniciar_juego, font=("Arial", 16, "bold"), bg="#1A5276", fg="white", padx=20, pady=10).pack(side=tk.LEFT, padx=30)
        tk.Button(btn_frame, text="SALIR DEL JUEGO", command=self.destroy, font=("Arial", 16, "bold"), bg="#707B7C", fg="white", padx=20, pady=10).pack(side=tk.LEFT, padx=30)


    def reiniciar_juego(self):
        """Reinicia el estado del juego y vuelve a la bienvenida."""
        self.escenario_actual = 0
        self.pistas = {"culpable": [], "locacion": [], "arma": []}
        self.culpable, self.locacion, self.arma = random.choice(FINALES) 
        self.mostrar_bienvenida()

if __name__ == "__main__":
    app = CruceroAlAcecho()
    app.update() 
    app.mostrar_bienvenida()
    app.mainloop()