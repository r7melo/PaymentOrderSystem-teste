import os
from nicegui import ui
from pages.login import render_login
from pages.home import render_home

@ui.page("/")
def login_page():
    render_login()

@ui.page("/home")
def home_page():
    render_home()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 80)),
        title="PaymentOrderSystem",
        storage_secret=os.getenv("STORAGE_SECRET", "payment-order-system-dev"),
        reload=True,
    )