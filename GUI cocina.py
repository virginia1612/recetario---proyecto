import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import json

# Creación de la ventana principal y su tamaño
ventana = tk.Tk()
ventana.title("Recetario")
ventana.geometry("1000x800")

# Creación de una imagen de fondo usando la librería PIL
imagen_fondo = ImageTk.PhotoImage(Image.open("pineapple-pizza.png"))
etiqueta_fondo = tk.Label(ventana, image=imagen_fondo)
etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Creación del menú desplegable
menu = tk.Menu(ventana)
menu_archivo = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Archivo de recetas", menu=menu_archivo)
ventana.config(menu=menu)

# Creación del archivo json  ## Aquí  hay que cambiar el contenido de la receta y agregar los items de la consigna
recetas = [
    {
        "nombre": "Ensalada de frutas",
        "ingredientes": ["manzana", "naranja", "banana", "fresas"],
        "cantidad": [1, 1, 2, 5],
        "Unidad": ["u", "u","u","u","u"],
        "Tiempo de preparacion": [15],
        "Tiempo de coccion": [0],
        "preparacion": "Lavar y cortar las frutas. \nMezclar en un recipiente y servir."
    },
    {
        "nombre": "Tarta de queso",
        "ingredientes": ["queso crema", "huevos", "azúcar", "harina"],
        "preparacion": "Batir el queso crema con los huevos y el azúcar. Agregar la harina y mezclar bien. Verter la mezcla en un molde y hornear durante 40 minutos a 180°C."
    }
]
recetario_json = json.dumps(recetas, indent=4)

def mostrar_recetario():
    messagebox.showinfo("Recetario", recetario_json)
menu_archivo.add_command(label="Ver todas las recetas", command=mostrar_recetario)

def eliminar_receta():
    # Pedir al usuario el nombre de la receta a eliminar
    nombre_receta = tk.simpledialog.askstring("Eliminar receta", "Ingrese el nombre de la receta que desea eliminar:")
    if nombre_receta is None:
        return  # el usuario canceló la operación

    # buscar la receta en la lista de recetas
    indice_receta = None
    for i, receta in enumerate(recetas):
        if receta["nombre"] == nombre_receta.lower():
            indice_receta = i
            break

    # si se encontró la receta, eliminarla
    if indice_receta is not None:
        recetas.pop(indice_receta)
        messagebox.showinfo("Recetario", f"La receta {nombre_receta} ha sido eliminada.")
    else:
        messagebox.showwarning("Recetario", f"No se encontró la receta {nombre_receta}.")      
menu_archivo.add_command(label="Eliminar una receta", command=eliminar_receta)

def modificar_receta():
    # pedir al usuario el nombre de la receta a modificar
    nombre_receta = tk.simpledialog.askstring("Modificar receta", "Ingrese el nombre de la receta que desea modificar:")
    if nombre_receta is None:
        return  # el usuario canceló la operación

    # buscar la receta en la lista de recetas
    indice_receta = None
    for i, receta in enumerate(recetas):
        if receta["nombre"] == nombre_receta:
            indice_receta = i
            break

    # si se encontró la receta, mostrar un cuadro de diálogo para modificarla
    if indice_receta is not None:
        nueva_receta = dict(receta)  # hacer una copia de la receta original
        nueva_receta["nombre"] = tk.simpledialog.askstring("Modificar receta", "Ingrese el nuevo nombre de la receta:", initialvalue=nueva_receta["nombre"])
        nueva_receta["ingredientes"] = tk.simpledialog.askstring("Modificar receta", "Ingrese los nuevos ingredientes de la receta (separados por comas):", initialvalue=", ".join(nueva_receta["ingredientes"])).split(", ")
        nueva_receta["preparacion"] = tk.simpledialog.askstring("Modificar receta", "Ingrese la nueva preparación de la receta:", initialvalue=nueva_receta["preparacion"])
        recetas[indice_receta] = nueva_receta
        messagebox.showinfo("Recetario", f"La receta {nombre_receta} ha sido modificada.")
    else:
        messagebox.showwarning("Recetario", f"No se encontró la receta {nombre_receta}.")

menu_archivo.add_command(label="Modificar una receta", command=modificar_receta)


# Creación de los widgets de la ventana
etiqueta_titulo = tk.Label(ventana, text="Crear receta: Nombre del plato")
entrada_titulo = tk.Entry(ventana)
etiqueta_ingredientes = tk.Label(ventana, text="Ingredientes")
texto_ingredientes = tk.Text(ventana, height=5, width=25)
etiqueta_pasos = tk.Label(ventana, text="Pasos")
texto_pasos = tk.Text(ventana, height=5, width=25)
boton_agregar = tk.Button(ventana, text="Agregar")
boton_recetadeldia=tk.Button(ventana,text="Pizza de ananá")   ##

opciones = ["Nombre", "Etiquetas", "Tiempo de preparación","Ingredientes",]
var_opciones = tk.StringVar(value=opciones[0])

etiqueta_opciones = tk.Label(ventana, text="Buscar recetas por:")
menu_opciones = tk.OptionMenu(ventana, var_opciones, *opciones)

etiqueta_titulo.grid(row=0, column=0)
entrada_titulo.grid(row=0, column=1)
etiqueta_ingredientes.grid(row=1, column=0)
texto_ingredientes.grid(row=1, column=1)
etiqueta_pasos.grid(row=2, column=0)
texto_pasos.grid(row=2, column=1)
boton_agregar.grid(row=3, column=1)
boton_recetadeldia.grid(row=9,column=3)   ##
etiqueta_opciones.grid(row=20, column=0)
menu_opciones.grid(row=20, column=1)
##
etiqueta_ejemplo = tk.Label(ventana, text="Receta del día")
etiqueta_ejemplo.grid(row=9, column=2)


def agregar_receta():
    nueva_receta = {
        "nombre": entrada_titulo.get(),
        "ingredientes": texto_ingredientes.get("1.0", "end-1c").split("\n"),
        "preparacion": texto_pasos.get("1.0", "end-1c")
        }
    recetas.append(nueva_receta)
    with open("recetas.json", "w") as archivo:
        json.dump(recetas, archivo, indent=4)
    messagebox.showinfo("Recetario", "Receta agregada con éxito.")
    entrada_titulo.delete(0, tk.END)
    texto_ingredientes.delete("1.0", tk.END)
    texto_pasos.delete("1.0", tk.END)
    
boton_agregar = tk.Button(ventana, text="Agregar", command=agregar_receta)
##
def busqueda_receta():
    texto_busqueda = entrada_busqueda.get()
    resultados = []
    for receta in recetas:
        if texto_busqueda.lower() in receta['nombre'].lower():
            resultados.append(receta['nombre'])
    if len(resultados) > 0:
        messagebox.showinfo("Recetario", f"Se encontraron {len(resultados)} recetas:\n\n{', '.join(resultados)}")
    else:
        messagebox.showinfo("Recetario", "No se encontraron recetas que coincidan con la búsqueda.")
##
## Buscador y filtro 
ventana.mainloop()
