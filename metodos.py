import customtkinter as ctk  # Importa la librería para la interfaz gráfica moderna.
from tkinter import messagebox  # Importa el módulo para mostrar alertas de error.
import numpy as np  # Importa la librería para manejo de arreglos y cálculos.
from scipy.interpolate import lagrange, interp1d  # Importa las funciones matemáticas de interpolación.
import matplotlib.pyplot as plt  # Importa el módulo para generar las gráficas.

ctk.set_appearance_mode("System")  # Configura el tema visual según el sistema operativo.

class App(ctk.CTk):  # Define la clase principal heredando de la ventana de CustomTkinter.
    def __init__(self):  # Método que inicializa la aplicación al crear el objeto.
        super().__init__()  # Inicializa la clase padre para configurar la ventana.
        self.title("Calculadora de Interpolación")  # Define el texto de la barra de título.
        self.geometry("400x650")  # Establece el tamaño inicial de la ventana en píxeles.

        ctk.CTkLabel(self, text="Valores de las x (separados por ,): ").pack(pady=5)  # Texto indicativo para el eje X.
        self.entry_x = ctk.CTkEntry(self, width=250)  # Campo de texto para capturar los datos de X.
        self.entry_x.pack()  # Ubica el campo de texto en la interfaz.

        ctk.CTkLabel(self, text="Valores de las f(x) (separados por ,): ").pack(pady=5)  # Esto hace lo mismo que la línea 14, pero para f(x).
        self.entry_y = ctk.CTkEntry(self, width=250)  # Esto hace lo mismo que la línea 15, pero para los datos de Y.
        self.entry_y.pack()  # Esto hace lo mismo que la línea 16.

        ctk.CTkLabel(self, text="Valor a buscar: ").pack(pady=5)  # Esto hace lo mismo que la línea 14, pero para el objetivo.
        self.entry_target = ctk.CTkEntry(self, width=150)  # Crea un campo más pequeño para el valor a interpolar.
        self.entry_target.pack()  # Esto hace lo mismo que la línea 16.

        self.switch_inv = ctk.CTkSwitch(self, text="¿Invertir variables?")  # Interruptor para intercambiar ejes X e Y.
        self.switch_inv.pack(pady=10)  # Ubica el interruptor con margen vertical.

        self.menu_op = ctk.CTkOptionMenu(self, values=["Lineal", "Cuadrática", "Lagrange"])  # Menú desplegable para elegir el algoritmo.
        self.menu_op.pack(pady=10)  # Esto hace lo mismo que la línea 27.

        self.check_graficar = ctk.CTkCheckBox(self, text="¿Grafica?")  # Casilla para decidir si se muestra la ventana de Matplotlib.
        self.check_graficar.pack(pady=10)  # Esto hace lo mismo que la línea 27.

        self.btn_calc = ctk.CTkButton(self, text="Calcular", command=self.calcular)  # Botón que dispara la función de cálculo.
        self.btn_calc.pack(pady=10)  # Esto hace lo mismo que la línea 27.

        self.result_label = ctk.CTkLabel(self, text="Resultado: ", font=("Arial", 16, "bold"))  # Etiqueta para mostrar el valor final.
        self.result_label.pack(pady=10)  # Esto hace lo mismo que la línea 27.

    def calcular(self):  # Define el proceso principal de lógica matemática.
        try:  # Inicia bloque para capturar errores de entrada de usuario.
            x_str = self.entry_x.get().split(',')  # Convierte el texto de X en una lista separada por comas.
            y_str = self.entry_y.get().split(',')  # Esto hace lo mismo que la línea 41, pero para Y.

            if len(x_str) != len(y_str):  # Verifica que ambas listas tengan la misma cantidad de datos.
                messagebox.showerror("Error", "X y f(x) deben tener igual longitud.")  # Muestra aviso si los datos están incompletos.
                return  # Detiene la ejecución si hay error de longitud.

            val_a = np.array([float(i) for i in x_str])  # Convierte la lista de texto X en números decimales.
            val_b = np.array([float(i) for i in y_str])  # Esto hace lo mismo que la línea 47, pero para la lista Y.
            target = float(self.entry_target.get())  # Convierte el valor de búsqueda en número decimal.

            if self.switch_inv.get():  # Revisa si el usuario activó la inversión de variables.
                x_data, y_data = val_b, val_a  # Intercambia los arreglos de datos.
                lbl_x, lbl_y = "Y", "X"  # Cambia los nombres de los ejes para la gráfica.
            else:  # Si el interruptor está apagado.
                x_data, y_data = val_a, val_b  # Mantiene el orden original de los datos.
                lbl_x, lbl_y = "X", "Y"  # Mantiene los nombres de ejes estándar.

            idx = np.argsort(x_data)  # Obtiene los índices necesarios para ordenar X de menor a mayor.
            x_data, y_data = x_data[idx], y_data[idx]  # Reordena ambos arreglos basándose en el orden de X.

            tipo = self.menu_op.get()  # Obtiene la opción seleccionada en el menú desplegable.
            if tipo == "Lineal":  # Si se eligió el método lineal.
                f = interp1d(x_data, y_data, kind='linear', fill_value="extrapolate")  # Crea función de interpolación de primer grado.
            elif tipo == "Cuadrática":  # Si se eligió el método cuadrático.
                f = interp1d(x_data, y_data, kind='quadratic', fill_value="extrapolate")  # Crea función de interpolación de segundo grado.
            else:  # En caso de elegir "Lagrange".
                f = lagrange(x_data, y_data)  # Genera el polinomio de Lagrange usando todos los puntos.

            res = f(target)  # Evalúa la función generada en el valor objetivo.
            self.result_label.configure(text=f"Resultado: {res:.4f}")  # Actualiza la interfaz con el resultado (4 decimales).

            if self.check_graficar.get():  # Revisa si la casilla de gráfica está marcada.
                self.mostrar_grafica(x_data, y_data, f, target, res, lbl_x, lbl_y)  # Llama a la función de dibujo.

        except ValueError:  # Se ejecuta si el usuario ingresó letras en lugar de números.
            messagebox.showerror("Error", "Ingresa solo números válidos.")  # Muestra alerta de formato incorrecto.
        except Exception as e:  # Captura cualquier otro error técnico inesperado.
            messagebox.showerror("Error", f"Detalle: {e}")  # Muestra el mensaje técnico del error.

    def mostrar_grafica(self, x, y, f, target, res, label_x, label_y):  # Define cómo dibujar la gráfica.
        plt.figure(figsize=(6, 4))  # Crea una nueva figura de Matplotlib con tamaño específico.
        x_range = np.linspace(x.min() - 1, x.max() + 1, 100)  # Genera 100 puntos para que la curva se vea suave.
        plt.plot(x_range, f(x_range), label="Función", color='blue')  # Dibuja la línea de la interpolación.
        plt.scatter(x, y, color='red', label="Datos")  # Dibuja los puntos originales como puntos rojos.
        plt.scatter(target, res, color='green', label="Búsqueda")  # Resalta el punto calculado en verde.
        plt.xlabel(label_x)  # Pone nombre al eje horizontal.
        plt.ylabel(label_y)  # Pone nombre al eje vertical.
        plt.legend()  # Muestra el cuadro de descripción de colores.
        plt.grid(True)  # Activa la cuadrícula de fondo.
        plt.show()  # Abre la ventana con la gráfica resultante.

if __name__ == "__main__":  # Verifica que el script se esté ejecutando directamente.
    app = App()  # Crea la instancia de la aplicación.
    app.mainloop()  # Inicia el ciclo de eventos para mantener la ventana abierta.