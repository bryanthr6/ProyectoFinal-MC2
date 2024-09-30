import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

class AdivinacionCartasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("201701010 - MC2 - Proyecto Final")

        # Cambiar el ícono de la ventana
        self.root.iconbitmap("FIUSAC.ico")  # Archivo .ico

        # Cambiar el color de fondo de la ventana principal
        self.root.configure(bg="#006691")  #color azul claro

        # Cargar las imágenes
        self.logo = tk.PhotoImage(file="Usac_logo.png")
        self.guess_image = tk.PhotoImage(file="guess.png")

        # Crear un marco para la imagen y el texto
        self.logo_frame = tk.Frame(root, bg="#006691")
        self.logo_frame.pack(pady=15)  # Margen vertical

        # Añadir la imagen USAC al marco
        self.logo_label = tk.Label(self.logo_frame, image=self.logo, bg="#006691")
        self.logo_label.pack(side=tk.LEFT)  # Alinear a la izquierda

        # Añadir la imagen de adivinanza al marco
        self.guess_label = tk.Label(self.logo_frame, image=self.guess_image, bg="#006691")
        self.guess_label.pack(side=tk.RIGHT, padx=10)  # Alinear a la derecha con un margen a la izquierda

        # Crear las etiquetas
        self.label_titulo = tk.Label(self.logo_frame, text="ADIVINACIÓN DE CARTAS EN GRUPOS DE 3", bg="#006691", fg="white", font=("Helvetica", 12, "bold"))
        self.label_titulo.pack(side=tk.LEFT, padx=10)  # Margen a la derecha de la imagen

        self.label_numero_cartas = tk.Label(root, text="Selecciona el número de cartas:", bg="#006691", fg="white", font=("Helvetica", 12, "bold"))
        self.label_numero_cartas.pack(pady=15)  # Margen vertical

        # Crear la ComboBox para seleccionar el número de cartas
        self.num_cartas_var = tk.StringVar()
        self.num_cartas_combobox = ttk.Combobox(root, textvariable=self.num_cartas_var, state="readonly", font=("Arial", 12, "bold"))
        self.num_cartas_combobox['values'] = (3, 9, 15, 21, 27, 33, 39)  # Valores disponibles en el combo box
        self.num_cartas_combobox.current(0)  # Establecer el valor predeterminado en 3
        self.num_cartas_combobox.pack(pady=10)  # Margen vertical
        
        self.start_button = tk.Button(root, text="Comenzar", command=self.iniciar_adivinacion, font=("Arial", 12, "bold"))
        self.start_button.pack(pady=10)  # Margen vertical

        # Añadir una etiqueta para mostrar el número de tirada
        self.tirada_label = tk.Label(root, text="", bg="#006691", fg="white", font=("Arial", 14, "bold"))
        self.tirada_label.pack(pady=10)  # Margen vertical
        
        self.grupos_frame = tk.Frame(root, bg="#006691")
        self.grupos_frame.pack(pady=6)  # Margen vertical para los grupos

        self.result_label = tk.Label(root, text="", bg="#006691")
        self.result_label.pack(pady=9)

        # Crear el enlace de créditos
        self.creditos_label = tk.Label(root, text="Créditos", bg="#006691", fg="white", font=("Arial", 10, "underline"), cursor="hand2")
        self.creditos_label.pack(side=tk.BOTTOM, pady=15)  # Alinear al fondo con margen vertical
        self.creditos_label.bind("<Button-1>", self.mostrar_creditos)  # Asociar clic a la función


        self.seleccion = None  # Guardará la selección de grupo

    def mostrar_creditos(self, event):
        # Mostrar un cuadro de diálogo con la información del autor
        messagebox.showinfo("Créditos", "Proyecto Final\nNombre: Bryant Herrera Rubio\nCarnet Universitario: 201701010\nMatemática para Computación 2 Sección N")

    def mezclar_y_dividir(self, cartas):
        return [cartas[i::3] for i in range(3)]

    def generar_cartas_aleatorias(self, cantidad):
        return random.sample(range(1, cantidad + 1), cantidad)

    def mostrar_grupos(self, grupos):
        # Limpiar el marco de grupos de la interfaz anterior
        for widget in self.grupos_frame.winfo_children():
            widget.destroy()

        # Mostrar cada grupo
        for i, grupo in enumerate(grupos):
            grupo_label = tk.Label(self.grupos_frame, text=f"Grupo {i+1}: {grupo}", 
                                bg="#006691", fg="white", font=("Verdana", 9, "bold"))
            grupo_label.pack(pady=3)  # Margen vertical

        # Nueva etiqueta que se mostrará después de los grupos
        seleccion_label = tk.Label(self.grupos_frame, text="Selecciona el grupo donde se encuentra tu carta:", 
                                    bg="#006691", fg="white", font=("Verdana", 10, "bold"))
        seleccion_label.pack(pady=5)  # Margen vertical

        # Crear los botones de opción (radio buttons)
        self.seleccion_var = tk.IntVar()
        for i in range(3):
            tk.Radiobutton(self.grupos_frame, text=f"Grupo {i+1}", variable=self.seleccion_var, 
                        value=i, bg="#006691", font=("Verdana", 12)).pack()

        # Botón para seleccionar el grupo
        self.next_button = tk.Button(self.grupos_frame, text="Seleccionar", 
                                    command=self.seleccionar_grupo, font=("Arial", 12, "bold"))
        self.next_button.pack(pady=0)  # Margen vertical

    def reorganizar_cartas(self, grupos, seleccion):
        if seleccion == 0:
            return grupos[1] + grupos[0] + grupos[2]
        elif seleccion == 2:
            return grupos[0] + grupos[2] + grupos[1]
        else:
            return grupos[0] + grupos[1] + grupos[2]

    def seleccionar_grupo(self):
        self.seleccion = self.seleccion_var.get()
        self.adivinacion_tirada()

    def iniciar_adivinacion(self):
        # Limpiar el resultado anterior
        self.result_label.config(text="")

        # Obtener el número de cartas seleccionado desde la ComboBox
        num_cartas = int(self.num_cartas_var.get())
        self.num_cartas = num_cartas
        self.cartas = self.generar_cartas_aleatorias(num_cartas)

        # Definir el número de tiradas necesarias
        if num_cartas == 3:
            self.num_tiradas = 1
        elif num_cartas == 9:
            self.num_tiradas = 2
        elif num_cartas == 39:
            self.num_tiradas = 4
        elif num_cartas == 33:
            self.num_tiradas = 4
        else:
            self.num_tiradas = 3  # Para 15, 21, 27,

        self.tirada = 0
        self.adivinacion_tirada()

    def adivinacion_tirada(self):
        if self.tirada < self.num_tiradas:
            # Actualizar el contador de tiradas
            self.tirada_label.config(text=f"Tirada {self.tirada + 1}")
            self.tirada_label.pack(pady=2)  # Margen vertical
            
            # Mostrar los grupos y permitir la selección
            if self.tirada == 0:
                self.grupos = self.mezclar_y_dividir(self.cartas)  # Primera vez, mezcla las cartas
            else:
                self.cartas = self.reorganizar_cartas(self.grupos, self.seleccion)
                self.grupos = self.mezclar_y_dividir(self.cartas)
                
            self.mostrar_grupos(self.grupos)
            self.tirada += 1
        else:
            # Fin del proceso, adivinar la carta
            self.cartas = self.reorganizar_cartas(self.grupos, self.seleccion)
            posicion_carta = len(self.cartas) // 2
            carta_adivinada = self.cartas[posicion_carta]

            # Mostrar la carta en un cuadro de diálogo emergente
            messagebox.showinfo("Carta Adivinada", f"La carta que pensaste es: {carta_adivinada}")


if __name__ == "__main__":
    root = tk.Tk()

    # Establecer el tamaño de la ventana principal (ancho x alto)
    window_width = 700
    window_height = 600

    # Obtener el tamaño de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcular la posición centrada
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Establecer la geometría de la ventana con la posición calculada
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y-35}")

    # Deshabilitar la opción de redimensionar la ventana
    root.resizable(False, False)

    app = AdivinacionCartasApp(root)
    root.mainloop()