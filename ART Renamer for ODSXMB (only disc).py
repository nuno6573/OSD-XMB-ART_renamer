import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

def validate_png(file_path):
    """Checks if a file is PNG."""
    return file_path.lower().endswith('.png')

def get_valid_directory(title):
    """Requests a directory path graphically."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    path = filedialog.askdirectory(title=title)
    root.destroy()
    if not path:
        print("Error: No folder selected. The script will exit.")
        exit()
    if not os.path.isdir(path):
        print(f"Error: The path {path} is not a valid directory.")
        exit()
    return path

def create_art_folder(osdxmb_path):
    """Create the ART folder if it doesn't exist."""
    art_path = os.path.join(osdxmb_path, "ART")
    if not os.path.exists(art_path):
        os.makedirs(art_path)
        print(f"ART folder created in: {art_path}")
    return art_path

def process_images(opl_path, art_path):
    """Processes images and organizes them into folders in PS2 Classic format."""
    # Lista de archivos en la carpeta de OPL Manager
    files = [f for f in os.listdir(opl_path) if validate_png(f)]
    
    if not files:
        print("Error: No PNG files were found in the specified path.")
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
            print(f"Warning: The file {file} does not follow the expected format (ID_TYPE.png). Ignored.")
    
    # Procesar cada juego
    for game_id, images in game_images.items():
        # Crear carpeta para el juego (reemplazar espacio por guion bajo si aplica)
        game_folder = game_id.replace(' ', '_')
        game_folder_path = os.path.join(art_path, game_folder)
        os.makedirs(game_folder_path, exist_ok=True)
        
        # Mapa de correspondencias
        mappings = {
            'ICO': 'ICON0.PNG'
        }
        
        # Copiar y renombrar imágenes
        for img_type, src_file in images.items():
            if img_type in mappings:
                dst_file = os.path.join(game_folder_path, mappings[img_type])
                shutil.copy(os.path.join(opl_path, src_file), dst_file)
                print(f"Processing: {src_file} -> {dst_file}")
            else:
                print(f"Warning: Image type {img_type} not recognized for {game_id}. Ignored.")
        
        # Verificar que las tres imágenes requeridas estén presentes
        required_images = ['ICON0.PNG']
        for img in required_images:
            if not os.path.exists(os.path.join(game_folder_path, img)):
                print(f"Warning: {img} is missing in {game_folder} folder.")
    
    return True

def show_final_message():
    """Display a final message and wait for the user to click a button."""
    root = tk.Tk()
    root.title("Process Completed")
    root.geometry("400x200")  # Ventana más grande para evitar que el botón se corte
    root.resizable(False, False)  # Evitar redimensionar
    label = tk.Label(root, text="by nuno6573 (from VizoR file)\nPress button to confirm", font=("Arial", 12))
    label.pack(pady=30)
    button = tk.Button(root, text="Confirm", command=root.quit, width=10, height=2)
    button.pack(pady=20)
    root.mainloop()

def main():
    # Crear ventana raíz para tkinter
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    
    # Solicitar rutas de forma gráfica
    opl_path = get_valid_directory("Select the folder with the OPL Manager images")
    osdxmb_path = get_valid_directory("Select the OSDXMB folder")
    
    # Verificar y crear carpeta ART
    art_path = create_art_folder(osdxmb_path)
    
    # Procesar imágenes
    print("Processing images...")
    success = process_images(opl_path, art_path)
    
    # Mostrar mensaje final si el procesamiento fue exitoso
    if success:
        print("\nProcessing completed!")
        show_final_message()
    else:
        print("Error: Processing failed. Review the warning messages.")
    
    root.destroy()

if __name__ == "__main__":
    main()