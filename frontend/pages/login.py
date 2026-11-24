from nicegui import app, ui
import httpx
from services.api import GatewayClient, extract_error_message


def render_login():
    if app.storage.user.get("token"):
        ui.navigate.to("/home")
        return

    with ui.column().classes("w-full h-screen items-center justify-center bg-slate-100"):
        with ui.card().classes("w-96 p-6 shadow-lg"):
            ui.label("PaymentOrderSystem").classes("text-2xl font-bold text-slate-800 mb-1")
            ui.label("Acesse sua conta via Gateway").classes("text-sm text-slate-500 mb-4")

            with ui.tabs().classes("w-full") as tabs:
                login_tab = ui.tab("Entrar")
                register_tab = ui.tab("Criar Conta")

            with ui.tab_panels(tabs, value=login_tab).classes("w-full mt-2"):
                # Aba de Login
                with ui.tab_panel(login_tab):
                    email_in = ui.input("E-mail").classes("w-full mb-2")
                    pass_in = ui.input("Senha", password=True, password_toggle_button=True).classes("w-full mb-4")

                    async def handle_login():
                        if not email_in.value or not pass_in.value:
                            ui.notify("Preencha e-mail e senha.", type="warning")
                            return
                        try:
                            client = GatewayClient()
                            data = await client.login(email_in.value, pass_in.value)
                            user_info = data.get("user", {})

                            app.storage.user["token"] = data["access_token"]
                            app.storage.user["user_id"] = user_info.get("id")
                            app.storage.user["user_name"] = user_info.get("name", "")
                            app.storage.user["user_email"] = user_info.get("email", email_in.value)

                            ui.notify(f"Bem-vindo, {app.storage.user['user_name']}!", type="positive")
                            ui.navigate.to("/home")
                        except httpx.HTTPStatusError as e:
                            ui.notify(extract_error_message(e), type="negative")
                        except Exception:
                            ui.notify("Gateway indisponível no momento.", type="negative")

                    ui.button("Entrar", on_click=handle_login).classes("w-full bg-blue-600 text-white")

                # Aba de Cadastro
                with ui.tab_panel(register_tab):
                    name_reg = ui.input("Nome completo").classes("w-full mb-2")
                    email_reg = ui.input("E-mail").classes("w-full mb-2")
                    pass_reg = ui.input("Senha", password=True, password_toggle_button=True).classes("w-full mb-4")

                    async def handle_register():
                        if not name_reg.value or not email_reg.value or not pass_reg.value:
                            ui.notify("Preencha todos os campos.", type="warning")
                            return
                        try:
                            client = GatewayClient()
                            await client.register(name_reg.value, email_reg.value, pass_reg.value)
                            ui.notify("Conta criada com sucesso! Faça login.", type="positive")
                            email_in.value = email_reg.value
                            name_reg.value = ""
                            email_reg.value = ""
                            pass_reg.value = ""
                            tabs.set_value(login_tab)
                        except httpx.HTTPStatusError as e:
                            ui.notify(extract_error_message(e), type="negative")
                        except Exception:
                            ui.notify("Gateway indisponível no momento.", type="negative")

                    ui.button("Cadastrar", on_click=handle_register).classes("w-full bg-emerald-600 text-white")