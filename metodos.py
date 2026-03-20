import customtkinter as ctk  # Librería para crear interfaces gráficas modernas.
from tkinter import messagebox  # Permite mostrar mensajes de error o advertencia.
import numpy as np  # Librería para trabajar con arreglos y cálculos numéricos.
from scipy.interpolate import lagrange, interp1d  # Métodos de interpolación.
import matplotlib.pyplot as plt  # Librería para generar gráficas.

ctk.set_appearance_mode("System")  # Ajusta el tema visual automáticamente.

class App(ctk.CTk):  # Clase principal de la aplicación.
    def __init__(self):  # Constructor de la ventana.
        super().__init__()
        self.title("Calculadora de Interpolación")  # Título de la ventana.
        self.geometry("420x700")  # Tamaño de la ventana.

        # ===== ENTRADAS =====

        ctk.CTkLabel(self, text="Valores de X (separados por ,):").pack(pady=5)
        self.entry_x = ctk.CTkEntry(self, width=250)  # Entrada para valores X.
        self.entry_x.pack()

        ctk.CTkLabel(self, text="Valores de f(x) (separados por ,):").pack(pady=5)
        self.entry_y = ctk.CTkEntry(self, width=250)  # Entrada para valores Y.
        self.entry_y.pack()

        ctk.CTkLabel(self, text="Valor a buscar:").pack(pady=5)
        self.entry_target = ctk.CTkEntry(self, width=150)  # Valor objetivo.
        self.entry_target.pack()

        ctk.CTkLabel(self, text="Valor exacto de f(x) (opcional):").pack(pady=5)
        self.entry_exact = ctk.CTkEntry(self, width=150)  # Para calcular error.
        self.entry_exact.pack()

        # Interruptor para interpolación inversa
        self.switch_inv = ctk.CTkSwitch(self, text="Interpolación inversa")
        self.switch_inv.pack(pady=10)

        # ===== MENÚ DE OPCIONES =====

        self.menu_op = ctk.CTkOptionMenu(
            self,
            values=[
                "Lineal",
                "Cuadrática",
                "Lagrange 1er grado",
                "Lagrange 2do grado"
            ]
        )
        self.menu_op.pack(pady=10)

        # Checkbox para mostrar gráfica
        self.check_graficar = ctk.CTkCheckBox(self, text="Mostrar gráfica")
        self.check_graficar.pack(pady=10)

        # Botón de cálculo
        self.btn_calc = ctk.CTkButton(self, text="Calcular", command=self.calcular)
        self.btn_calc.pack(pady=10)

        # ===== SALIDAS =====

        self.result_label = ctk.CTkLabel(self, text="Resultado:", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=10)

        self.error_label = ctk.CTkLabel(self, text="", font=("Arial", 12))  # Error porcentual.
        self.error_label.pack(pady=5)

        self.warning_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12, "bold"),
            text_color="red"
        )  # Advertencia de extrapolación.
        self.warning_label.pack(pady=5)

    def calcular(self):  # Función principal que ejecuta los cálculos.
        try:
            tipo = self.menu_op.get()  # Obtiene el método seleccionado.

            # Convierte texto a listas separadas por coma
            x_str = self.entry_x.get().split(',')
            y_str = self.entry_y.get().split(',')

            # ===== VALIDACIONES =====

            if len(x_str) != len(y_str):  # Verifica que tengan igual tamaño.
                messagebox.showerror("Error", "X y f(x) deben tener igual longitud.")
                return

            if len(x_str) < 2:  # Se requieren al menos 2 puntos.
                messagebox.showerror("Error", "Se necesitan al menos 2 puntos.")
                return

            # Convierte a números
            x_data = np.array([float(i) for i in x_str])
            y_data = np.array([float(i) for i in y_str])
            target = float(self.entry_target.get())

            # ===== INTERPOLACIÓN INVERSA =====

            if self.switch_inv.get():
                x_data, y_data = y_data, x_data  # Intercambia datos.
                lbl_x, lbl_y = "Y", "X"
            else:
                lbl_x, lbl_y = "X", "Y"

            # Ordena los datos
            idx = np.argsort(x_data)
            x_data = x_data[idx]
            y_data = y_data[idx]

            # ===== DETECCIÓN DE EXTRAPOLACIÓN =====

            if target < x_data.min() or target > x_data.max():
                self.warning_label.configure(text="⚠ Advertencia: Extrapolación")
            else:
                self.warning_label.configure(text="")

            # ===== SELECCIÓN DE PUNTOS MÁS CERCANOS =====

            distancias = np.abs(x_data - target)  # Distancia al target.
            indices = np.argsort(distancias)  # Ordena de menor a mayor.

            # ===== MÉTODOS =====

            if tipo == "Lineal":
                f = interp1d(x_data, y_data, kind='linear', fill_value="extrapolate")

            elif tipo == "Cuadrática":
                if len(x_data) < 3:
                    messagebox.showerror("Error", "Se necesitan al menos 3 puntos.")
                    return
                f = interp1d(x_data, y_data, kind='quadratic', fill_value="extrapolate")

            elif tipo == "Lagrange 1er grado":
                puntos = indices[:2]  # Selecciona 2 puntos más cercanos.
                f = lagrange(x_data[puntos], y_data[puntos])

            elif tipo == "Lagrange 2do grado":
                if len(x_data) < 3:
                    messagebox.showerror("Error", "Se necesitan al menos 3 puntos.")
                    return
                puntos = indices[:3]  # Selecciona 3 puntos más cercanos.
                f = lagrange(x_data[puntos], y_data[puntos])

            # ===== RESULTADO =====

            resultado = f(target)
            self.result_label.configure(text=f"Resultado: {resultado:.4f}")

            # ===== ERROR PORCENTUAL =====

            valor_exacto = self.entry_exact.get()
            if valor_exacto:
                valor_exacto = float(valor_exacto)
                error = abs((valor_exacto - resultado) / valor_exacto) * 100
                self.error_label.configure(text=f"Error: {error:.2f}%")
            else:
                self.error_label.configure(text="")

            # ===== GRÁFICA =====

            if self.check_graficar.get():
                self.mostrar_grafica(x_data, y_data, f, target, resultado, lbl_x, lbl_y)

        except ValueError:
            messagebox.showerror("Error", "Ingresa solo números válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Detalle: {e}")

    def mostrar_grafica(self, x, y, f, target, resultado, label_x, label_y):
        plt.figure(figsize=(6, 4))  # Crea figura.

        x_range = np.linspace(x.min() - 1, x.max() + 1, 100)  # Rango para graficar.

        plt.plot(x_range, f(x_range), label="Interpolación")  # Curva.
        plt.scatter(x, y, label="Datos")  # Puntos originales.
        plt.scatter(target, resultado, label="Resultado")  # Punto calculado.

        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    app = App()  # Crea la app.
    app.mainloop()  # Ejecuta la interfaz.