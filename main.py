from tkinter import ttk
from tkinter import *
import sqlite3

class Producto:

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Gestor de productos")
        self.ventana.resizable(1,1)
        self.ventana.wm_iconbitmap("recursos/icono.ico")

        #Creacion del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo producto", labelanchor=N, font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=15)


        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13))
        self.etiqueta_nombre.grid(row=1, column=0, pady=22)
        #Entry Nombre
        self.nombre = Entry(frame, font=('Calibri', 13), insertbackground="gray", background="#f2f2f2")
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=2, column=0, pady=22)
        # Entry Precio
        self.precio = Entry(frame, font=('Calibri', 13), insertbackground="gray", background="#f2f2f2")
        self.precio.grid(row=2, column=1)

        # Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoria: ", font=('Calibri', 13))
        self.etiqueta_categoria.grid(row=3, column=0, pady=22)
        # Entry Precio
        self.categoria = Entry(frame, font=('Calibri', 13), insertbackground="gray", background="#f2f2f2")
        self.categoria.grid(row=3, column=1)

        # Label Stock
        self.etiqueta_stock = Label(frame, text="Stock: ", font=('Calibri', 13))
        self.etiqueta_stock.grid(row=4, column=0, pady=22)
        # Entry Stock
        self.stock = Entry(frame, font=('Calibri', 13), insertbackground="gray", background="#f2f2f2")
        self.stock.grid(row=4, column=1)

        #Boton de añadir producto
        self.boton_aniadir = Button(frame, text="GUARDAR PRODUCTO", height=2, command=self.add_producto, bg="lightgreen", fg="black", font=('Arial', 12, "bold"))
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W+E, pady=5)

        self.mensaje = Label(text="", fg="red", font=('Calibri', 12))
        self.mensaje.place(x=270, y=305)

        #Tabla productos
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 13))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':'nswe'})])  # Eliminamos los bordes

        #Estructura de la tabla
        self.tabla = ttk.Treeview(frame, height=20, columns=('#0', '#1', '#2'), style="mystyle.Treeview")
        self.tabla.grid(row=6, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1
        self.tabla.heading('#2', text='Categoria', anchor=CENTER)  # Encabezado 2
        self.tabla.heading('#3', text='Stock', anchor=CENTER)  # Encabezado 2

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure("my.TButton", font=('Calibri', 14, "bold"))

        boton_eliminar = Button(text='ELIMINAR', command=self.del_producto, bg="red", fg="black", height=2, width=40, font=('Arial', 12, "bold"))
        boton_eliminar.grid(row=7, column=0, columnspan=1, sticky=W + E)
        boton_editar = Button(text='EDITAR',command=self.edit_producto, bg="lightblue", fg="black", height=2, width=40, font=('Arial', 12, "bold"))
        boton_editar.grid(row=7, column=2, sticky=W + E)
        self.get_productos()

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)


        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila[1], values=(fila[2], fila[3], fila[4]))

    def validacion(self):
        return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0 and len(self.categoria.get()) != 0  and len(self.stock.get()) != 0

    def add_producto(self):
        if self.validacion():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)'  # Consulta SQL (sin los datos)
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())  # Parametros de la consulta SQL
            self.db_consulta(query, parametros)
            self.mensaje['text'] = 'Producto {} añadido con exito'.format(self.nombre.get()) # Label ubicado entre el boton y la tabla

            self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END)  # Borrar el campo precio del formulario
            self.categoria.delete(0, END)  # Borrar el campo categoria del formulario
            self.stock.delete(0, END)  # Borrar el campo stock del formulario
        else:
            self.mensaje['text'] = "Todos los campos son requeridos"
        self.get_productos()  # Cuando se finalice la insercion de datos volvemos a invocar a este metodo para actualizar el contenido y ver los cambios

    def del_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,))  # Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]  # El precio se encuentra dentro de una lista
        categoria = self.tabla.item(self.tabla.selection())['values'][1]    # La categoria se encuentra dentro de una lista
        stock = self.tabla.item(self.tabla.selection())['values'][2]    # El stock se encuentra dentro de una lista

        # Ventana nueva(editar producto)
        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana
        self.ventana_editar.resizable(1, 1)  # Activar la redimension de la ventana. Para desactivarla: (0, 0)
        self.ventana_editar.wm_iconbitmap('recursos/icono.ico')  # Icono de la ventana
        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'))  # frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_anituguo.grid(row=2, column=0)  # Posicionamiento a traves de grid

        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre),state='readonly', font=('Calibri', 13, 'bold'))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)

        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_anituguo = Label(frame_ep, text="Precio antiguo: ",font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_anituguo.grid(row=4, column=0)  # Posicionamiento a traves de grid

        # Entry Precio antiguo(texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),state='readonly', font=('Calibri', 13, 'bold'))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)

        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Categoria antigua
        self.etiqueta_categoria_antiugua = Label(frame_ep, text="Categoria antigua: ", font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_categoria_antiugua.grid(row=6, column=0)  # Posicionamiento a traves de grid

        # Entry Categoria antigua(texto que no se podra modificar)
        self.input_categoria_antiugua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=categoria),state='readonly', font=('Calibri', 13, 'bold'))
        self.input_categoria_antiugua.grid(row=6, column=1)

        # Label Categoria nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoria nueva: ", font=('Calibri', 13))
        self.etiqueta_categoria_nueva.grid(row=7, column=0)

        # Entry Categoria nuevo (texto que si se podra modificar)
        self.input_categoria_nueva = Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nueva.grid(row=7, column=1)

        # Label Stock antiguo
        self.etiqueta_stock_anituguo = Label(frame_ep, text="Stock antiguo: ",font=('Calibri', 13))  # Etiqueta de texto ubicada en el frame
        self.etiqueta_stock_anituguo.grid(row=8, column=0)  # Posicionamiento a traves de grid

        # Entry Stock antiguo(texto que no se podra modificar)
        self.input_stock_anituguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=stock), state='readonly', font=('Calibri', 13, 'bold'))
        self.input_stock_anituguo.grid(row=8, column=1)

        # Label Stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)

        # Entry Stock nuevo (texto que si se podra modificar)
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=9, column=1)



        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", command=lambda:
        self.actualizar_productos(self.input_nombre_nuevo.get(),
                                  self.input_nombre_antiguo.get(),
                                  self.input_precio_nuevo.get(),
                                  self.input_precio_antiguo.get(),
                                  self.input_categoria_nueva.get(),
                                  self.input_categoria_antiugua.get(),
                                  self.input_stock_nuevo.get(),
                                  self.input_stock_anituguo.get()))

        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)


    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio,antiguo_precio,nueva_categoria,antigua_categoria,nuevo_stock, antiguo_stock):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock = ? WHERE nombre = ? AND precio = ? AND categoria = ? AND stock = ?'
        if nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '': # Si el usuario escribe nuevo nombre,nuevo precio,nueva categoria y nuevo stock se cambian
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo nombre y el precio, se mantiene el nombre y el precio anterior
            parametros = (antiguo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo nombre, el precio y la categoria, se mantiene el nombre, el precio y la categoria anteriores
            parametros = (antiguo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo nombre y la categoria, se mantiene el nombre y la categoria anterior
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo nombre, la categoria y el stock, se mantiene el nombre y la categoria y el stock anterior
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo nombre y el stock, se mantiene el nombre y el stock anterior
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo nombre, el precio y el stock, se mantiene el nombre, el precio y el stock anterior
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el precio anterior
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '':
            # Si el usuario deja vacio el nuevo precio y la categoria, se mantiene el precio y la categoria anterior
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo precio, la categoria y el stock, se mantiene el precio, la categoria y el stock anterior
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo precio y el stock, se mantiene el precio y el stock anterior
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            # Si el usuario deja vacio la nueva categoria, se mantiene la categoria anterior
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '':
            # Si el usuario deja vacio la nueva categoria, se mantiene la categoria anterior
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria,antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock == '':
            # Si el usuario deja vacio el nuevo stock, se mantiene el stock anterior
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        if (producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre) # Mostrar mensaje para el usuario

if __name__ == "__main__":
    root = Tk() # Instancia de la ventana principal
    app = Producto(root)
    root.mainloop()
