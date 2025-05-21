# frontend/run.py
import flet as ft
from app.main import main  # Importa a função main de frontend/app/main.py

if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        port=8550, # Mesma porta do app/main.py para consistência
        assets_dir="app/assets" # Ajuste se a pasta assets estiver em frontend/assets
    )
    # Para desktop:
    # ft.app(target=main, assets_dir="app/assets")