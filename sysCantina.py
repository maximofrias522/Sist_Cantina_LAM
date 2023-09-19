import tkinter as tk
import tkinter.messagebox
import customtkinter
import sqlite3
import uuid
import time

def generate_unique_id():
    unique_id1 = str(uuid.uuid4()).replace('-', '')
    unique_id = unique_id1[:30]
    return unique_id

customtkinter.set_appearance_mode("Dark")  # Modos: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Temas: "blue" (standard), "green", "dark-blue"
customtkinter.set_window_scaling(1.5)
customtkinter.set_widget_scaling(1.2)


class App(customtkinter.CTk):
    db_name = 'DBCantina.db'

    def __init__(self):
        super().__init__()

        self.Resultado1 = tkinter.StringVar()

        # Configurar ventana
        self.title("Cantina LAM")
        self.geometry(f"{1100}x{580}")

        # Configurar disposicion de cuadro (4x5)
        self.grid_columnconfigure((1, 2, 3,), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure(1, weight=1)  # Columna 1 con peso 1 (expandible)
        self.grid_columnconfigure(2, weight=1)  # Columna 2 con peso 1 (expandible)
        self.grid_rowconfigure(0, weight=1)  # Fila 0 con peso 1 (expandible)
        self.grid_rowconfigure(1, weight=1)  # Fila 1 con peso 1 (expandible)
        self.grid_rowconfigure(2, weight=1)
        

        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Crear tabla para visualizar db Ventas
        self.treeview = tk.ttk.Treeview(self, columns=("Nro_Venta", "Descripcion_Producto", "Cantidad", "Precio_Total", "Transferencia_de", "Monto", "Fecha_y_hora"), show="headings", selectmode="browse")
        self.treeview.heading("Nro_Venta", text="ID de venta")
        self.treeview.heading("Descripcion_Producto", text="Descripcion de producto")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Precio_Total", text="Precio total")
        self.treeview.heading("Transferencia_de", text="Transferencia")
        self.treeview.heading("Monto", text="Monto")
        self.treeview.heading("Fecha_y_hora", text="Fecha y hora")
        self.treeview.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.style = tk.ttk.Style()
        self.style.configure("Treeview",
                             background="#D3D3D3",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#D3D3D3")
        self.style.map("Treeview",
                       background=[("selected", "#347083")],
                       foreground=[("selected", "white")],
                       relief=[("selected", "flat")])

        # Configuración de las líneas de separación en la tabla
        self.style.configure("Treeview.Heading", font=('Helvetica', 12, "bold"))
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Para tener líneas verticales y horizontales
        self.style.configure("Treeview.Heading", background="gray", foreground="black", bordercolor="black", lightcolor="gray", darkcolor="gray")
        self.treeview.grid(row=0, rowspan=3, column=1, columnspan=3, padx=(20, 20), pady=(20, 60), sticky="nsew")

        # Establecer el ancho de las columnas 
        self.treeview.column("Nro_Venta", width=30)
        self.treeview.column("Descripcion_Producto", width=130)
        self.treeview.column("Cantidad", width=20)
        self.treeview.column("Precio_Total", width=20)
        self.treeview.column("Transferencia_de", width=100)
        self.treeview.column("Monto", width=5)
        self.treeview.column("Fecha_y_hora", width=40)

        def on_double_click(event):
            item = self.treeview.selection()[0]
            selected_id = self.treeview.item(item)["values"][0]

            # Borrar de la GUI(self.treeview)
            self.treeview.delete(item)

            # Borrar de la DB (Ventas table)
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM Ventas WHERE Nro_Venta=?", (selected_id,))
                conn.commit()  # Commit cambios en DB
            finally:
                cursor.close()
                conn.close()

        self.treeview.bind("<Double-1>", on_double_click)

        # Recargar datos de tabla desde DB
        self.load_data_from_database1()

        # Crear elementos de entrada para la GUI
        self.input_transferencia_datos = customtkinter.CTkEntry(self, placeholder_text="Nombre y apellido")
        self.input_transferencia_datos.grid(row=2, column=1, columnspan=2, padx=(20,0), pady=(25,10), sticky="sew")

        self.input_monto = customtkinter.CTkEntry(self, placeholder_text="Monto Transferido")
        self.input_monto.grid(row=2, column=3, padx=(5,20), pady=(25,10), sticky="sew")

        self.input_description = customtkinter.CTkEntry(self, placeholder_text="Descripcion de producto")
        self.input_description.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="new")

        self.input_quantity = customtkinter.CTkEntry(self, placeholder_text="Cantidad")
        self.input_quantity.grid(row=3, column=3, padx=(5, 20), pady=(20, 20), sticky="new")

        self.input_description.bind("<KeyRelease>", lambda event: self.calculate_total_price())
        self.input_quantity.bind("<KeyRelease>", lambda event: self.calculate_total_price())


        # Crear boton de ingreso 
        self.submit_button = customtkinter.CTkButton(master=self, text="Cargar", command=self.submit_data)
        self.submit_button.grid(row=4, column=1, columnspan=3, padx=(20, 20), pady=(0, 20), sticky="new")

        # Crear barra laterar y visuales
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Cantina LAM", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Ventas",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30")
                                                   , anchor="w", command=self.home_button_event)
        self.sidebar_button_1.grid(row=1, column=0, sticky="ew")

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text="Stock",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.frame_2_button_event)
        self.sidebar_button_2.grid(row=2, column=0, sticky="ew")

        
        self.sidebar_firma = customtkinter.CTkLabel(self.sidebar_frame, text="Developed by Máximo Frías | V1.0", font=customtkinter.CTkFont(size=6))
        self.sidebar_firma.grid(row=7, column=0, padx=20, pady=(10, 0))

        #crear segundo frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.stock_treeview = tk.ttk.Treeview(self.second_frame, columns=("ID_producto", "Descripcion_Producto", "Precio_Unitario_Producto"), show="headings", selectmode="browse")
        self.stock_treeview.heading("ID_producto", text="ID de Producto")
        self.stock_treeview.heading("Descripcion_Producto", text="Descripcion de producto")
        self.stock_treeview.heading("Precio_Unitario_Producto", text="Precio Unitario")
        self.stock_treeview.grid(row=0, rowspan=3, column=1, columnspan=3, padx=(20, 20), pady=(20, 60), sticky="nsew")


        #Recargar datos de la tabla desde la DB
        self.load_data_from_database2()

        # select default frame
        self.select_frame_by_name("Ventas")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.sidebar_button_1.configure(fg_color=("gray75", "gray25") if name == "Ventas" else "transparent")
        self.sidebar_button_2.configure(fg_color=("gray75", "gray25") if name == "Stock" else "transparent")

        # show selected frame
        if name == "Ventas":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Stock":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("Ventas")

    def frame_2_button_event(self):
        self.select_frame_by_name("Stock")


    def load_data_from_database1(self):
        # Conectar a la DB
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Hacer query SELECT
            cursor.execute("SELECT Nro_Venta, Descripcion_Producto, Cantidad, Precio_Total, Transferencia_de, Monto, Fecha_y_hora FROM Ventas")

            # Borrar tabla de GUI
            self.treeview.delete(*self.treeview.get_children())

            # Insertar datos de DB en la tabla
            for row in cursor.fetchall():
                self.treeview.insert("", "end", values=row)

        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error fetching data from the database: {e}")
        finally:
            cursor.close()
            conn.close()

            self.treeview.yview_moveto(1)

    def calculate_total_price(self):
        description = self.input_description.get()
        quantity = int(self.input_quantity.get())  # Convertir a entero

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Obtener el precio del producto de la base de datos usando la descripción como referencia
            cursor.execute("SELECT Precio_Unitario_Producto FROM Stock WHERE Descripcion_Producto = ?", (description,))
            row = cursor.fetchone()
            if row is not None:
                precio_unitario = float(row[0])  # Convertir a número (float)
                total_price = precio_unitario * quantity
                self.Resultado1.set(total_price)  # Actualizar el valor en la variable StringVar
            else:
                tkinter.messagebox.showinfo("Información", "Producto no encontrado en la base de datos")

        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error al consultar datos en la base: {e}")

        finally:
            cursor.close()
            conn.close()

    def submit_data(self):
        description = self.input_description.get()
        quantity = int(self.input_quantity.get())
        transferencia = self.input_transferencia_datos.get()
        monto = self.input_monto.get()
        unique_id = generate_unique_id()
        ahora = time.strftime("%x") + " " + time.strftime("%X")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO Ventas (Nro_Venta, Descripcion_Producto, Cantidad, Precio_Total, Transferencia_de, Monto, Fecha_y_hora) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (unique_id, description, quantity, self.Resultado1.get(), transferencia, monto, ahora))


            conn.commit()

            self.load_data_from_database1()
            self.input_description.delete(0, "end")
            self.input_quantity.delete(0, "end")
            self.input_monto.delete(0, "end")
            self.input_transferencia_datos.delete(0, "end")
        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error al insertar datos en la base: {e}")
            conn.rollback()

        finally:
            cursor.close()
            conn.close()




    def load_data_from_database2(self):
        # Conectar a la DB
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Ejecutar query SELECT
            cursor.execute("SELECT ID_producto, Descripcion_Producto, Precio_Unitario_Producto FROM Stock")

            # Borrar datos actuales en la tabla
            self.stock_treeview.delete(*self.stock_treeview.get_children())

            # Insertar datos desde la DB en la tabla 
            for row in cursor.fetchall():
                self.stock_treeview.insert("", "end", values=row)

        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error fetching data from the database: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()