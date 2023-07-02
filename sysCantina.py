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

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    db_name = 'DBCantina.db'

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Cantina LAM")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.grid_rowconfigure((0), weight=1)
       
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Cantina LAM 2023", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Ventas", command=self.sidebar_Ventas_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Stock", command=self.sidebar_Stock_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Cambiar Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tamaño de UI:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main treeview for database Ventas visualization
        self.treeview = tk.ttk.Treeview(self, columns=("Nro_Venta", "Descripcion_Producto", "Cantidad", "Precio_Total", "Transferencia", "Fecha_y_hora"), show="headings", selectmode="browse")
        self.treeview.heading("Nro_Venta", text="ID de venta")
        self.treeview.heading("Descripcion_Producto", text="Descripcion de producto")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Precio_Total", text="Precio total")
        self.treeview.heading("Transferencia", text="Transferencia")
        self.treeview.heading("Fecha_y_hora", text="Fecha y hora")
        self.treeview.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # Set the width of each column
        self.treeview.column("Nro_Venta", width=60)
        self.treeview.column("Descripcion_Producto", width=140)
        self.treeview.column("Cantidad", width=50)
        self.treeview.column("Precio_Total", width=70)
        self.treeview.column("Transferencia", width=80)
        self.treeview.column("Fecha_y_hora", width=75)

        # populate the treeview with data from the database
        self.load_data_from_database()

        # Create input fields (Entry widgets) for each column in the table
        self.input_description = customtkinter.CTkEntry(self, placeholder_text="Descripcion de producto")
        self.input_description.grid(row=1, column=1, padx=(20, 0), pady=(10, 20), sticky="nsew")

        self.input_quantity = customtkinter.CTkEntry(self, placeholder_text="Cantidad")
        self.input_quantity.grid(row=1, column=2, padx=(0, 0), pady=(10, 20), sticky="nsew")

        # Create checkbox for "transferencia validation"
        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="Transferencia")
        self.checkbox_1.grid(row=1, column=3, pady=(10, 0), padx=(10), sticky="n")

        # Create "Submit" button
        self.submit_button = customtkinter.CTkButton(master=self, text="Cargar", command=self.submit_data)
        self.submit_button.grid(row=2, column=1, columnspan=3, padx=(20, 20), pady=(0, 20), sticky="nsew")

    def submit_data(self):
        # Get the input data from the Entry widgets
        description = self.input_description.get()
        quantity = self.input_quantity.get()
        transferencia = "Sí" if self.checkbox_1.get() else "No" 

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def load_data_from_database(self):
        # Connect to the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Execute a SELECT query
            cursor.execute("SELECT Nro_Venta, Descripcion_Producto, Cantidad, Precio_Total, Transferencia, Fecha_y_hora FROM Ventas")

            # Clear existing data in the treeview
            self.treeview.delete(*self.treeview.get_children())

            # Insert data from the database into the treeview
            for row in cursor.fetchall():
                self.treeview.insert("", "end", values=row)

        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error fetching data from the database: {e}")

    def submit_data(self):
        # Get the input data from the Entry widgets
        description = self.input_description.get()
        quantity = self.input_quantity.get()
        transferencia = self.checkbox_1.get()
        unique_id = generate_unique_id()

    # Validate the data (you can add your own validation logic here)
        # if not description or not quantity or not transferencia:
        #     tkinter.messagebox.showwarning("Warning", "Please fill in all fields.")
        #     return
        
         # Connect to the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Insert the data into the "Ventas" table
            cursor.execute("INSERT INTO Ventas (Nro_Venta, Descripcion_Producto, Cantidad, Transferencia) VALUES (?, ?, ?, ?)",
                       (unique_id, description, quantity, transferencia))

            # Commit the transaction
            conn.commit()

            # Reload the data from the database and update the treeview
            self.load_data_from_database()

            # Clear the input fields after successfully inserting the data
            self.input_description.delete(0, "end")
            self.input_quantity.delete(0, "end")
            self.checkbox_1(False)

            tkinter.messagebox.showinfo("Success", "Datos ingresados correctamente.")

        except sqlite3.Error as e:
            tkinter.messagebox.showerror("Error", f"Error al insertar datos en la base: {e}")
            conn.rollback()

        finally:
            # Close the database connection
            cursor.close()
            conn.close()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_Ventas_event(self):
        print("sidebar ventas click")

    def sidebar_Stock_event(self):
        print("sidebar stock click")

if __name__ == "__main__":
    app = App()
    app.mainloop()