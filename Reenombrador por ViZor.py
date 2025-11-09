import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

def validate_png(file_path):
    """Verifica si un archivo es PNG."""
    return file_path.lower().endswith('.png')

def get_valid_directory(title):
    """Solicita una ruta de directorio de forma gráfica."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    path = filedialog.askdirectory(title=title)
    root.destroy()
    if not path:
        print("Error: No se seleccionó ninguna carpeta. El script se cerrará.")
        exit()
    if not os.path.isdir(path):
        print(f"Error: La ruta {path} no es un directorio válido.")
        exit()
    return path

def create_art_folder(osdxmb_path):
    """Crea la carpeta ART si no existe."""
    art_path = os.path.join(osdxmb_path, "ART")
    if not os.path.exists(art_path):
        os.makedirs(art_path)
        print(f"Carpeta ART creada en: {art_path}")
    return art_path

def process_images(opl_path, art_path):
    """Procesa las imágenes y las organiza en carpetas con el formato PS2 Classic."""
    # Lista de archivos en la carpeta de OPL Manager
    files = [f for f in os.listdir(opl_path) if validate_png(f)]
    
    if not files:
        print("Error: No se encontraron archivos PNG en la ruta especificada.")
        return False
    
    # Agrupar imágenes por ID de juego
    game_images = {}
    for file in files:
        # Ejemplo: SCES_516.07_ICO.png -> ID: SCES_516.07, Tipo: ICO
        try:
            game_id, img_type = file.rsplit('.', 1)[0].rsplit('_', 1)
            if game_id not in game_images:
                game_images[game_id] = {}
            game_images[game_id][img_type] = file
        except ValueError:
            print(f"Advertencia: El archivo {file} no sigue el formato esperado (ID_TIPO.png). Ignorado.")
    
    # Procesar cada juego
    for game_id, images in game_images.items():
        # Crear carpeta para el juego (reemplazar espacio por guion bajo si aplica)
        game_folder = game_id.replace(' ', '_')
        game_folder_path = os.path.join(art_path, game_folder)
        os.makedirs(game_folder_path, exist_ok=True)
        
        # Mapa de correspondencias
        mappings = {
            'ICO': 'ICON0.PNG',
            'BG': 'PIC1.PNG',
            'COV': 'PIC2.PNG'
        }
        
        # Copiar y renombrar imágenes
        for img_type, src_file in images.items():
            if img_type in mappings:
                dst_file = os.path.join(game_folder_path, mappings[img_type])
                shutil.copy(os.path.join(opl_path, src_file), dst_file)
                print(f"Procesado: {src_file} -> {dst_file}")
            else:
                print(f"Advertencia: Tipo de imagen {img_type} no reconocido para {game_id}. Ignorado.")
        
        # Verificar que las tres imágenes requeridas estén presentes
        required_images = ['ICON0.PNG', 'PIC1.PNG', 'PIC2.PNG']
        for img in required_images:
            if not os.path.exists(os.path.join(game_folder_path, img)):
                print(f"Advertencia: Falta {img} en la carpeta {game_folder}.")
    
    return True

def show_final_message():
    """Muestra un mensaje final y espera a que el usuario pulse un botón."""
    root = tk.Tk()
    root.title("Proceso Completado")
    root.geometry("400x150")  # Ventana más grande para evitar que el botón se corte
    root.resizable(False, False)  # Evitar redimensionar
    label = tk.Label(root, text="BY ViZoR Retrogames\nPulse un botón para confirmar", font=("Arial", 12))
    label.pack(pady=30)
    button = tk.Button(root, text="Confirmar", command=root.quit, width=10, height=2)
    button.pack(pady=20)
    root.mainloop()

def main():
    # Crear ventana raíz para tkinter
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    
    # Solicitar rutas de forma gráfica
    opl_path = get_valid_directory("Selecciona la carpeta con las imágenes de OPL Manager")
    osdxmb_path = get_valid_directory("Selecciona la carpeta OSDXMB")
    
    # Verificar y crear carpeta ART
    art_path = create_art_folder(osdxmb_path)
    
    # Procesar imágenes
    print("Procesando imágenes...")
    success = process_images(opl_path, art_path)
    
    # Mostrar mensaje final si el procesamiento fue exitoso
    if success:
        print("\n¡Procesamiento completado!")
        show_final_message()
    else:
        print("Error: El procesamiento falló. Revisa los mensajes de advertencia.")
    
    root.destroy()

if __name__ == "__main__":
    main()