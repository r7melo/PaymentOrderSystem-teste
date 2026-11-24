from nicegui import app, ui
import httpx
from services.api import GatewayClient


def render_home():
    token = app.storage.user.get("token")
    if not token:
        ui.navigate.to("/")
        return

    client = GatewayClient(token=token)

    def logout():
        app.storage.user.clear()
        ui.navigate.to("/")

    # Barra Superior
    with ui.header().classes("bg-slate-900 text-white items-center justify-between px-6"):
        ui.label("PaymentOrderSystem").classes("text-lg font-bold")
        with ui.row().classes("items-center gap-4"):
            user_label = ui.label(
                f"{app.storage.user.get('user_name', '')} ({app.storage.user.get('user_email', '')})"
            ).classes("text-sm text-slate-300")
            ui.button("Sair", on_click=logout, icon="logout").props("flat color=white")

    # Conteúdo Principal
    with ui.column().classes("w-full max-w-5xl mx-auto p-6 gap-6"):
        with ui.row().classes("w-full gap-6"):
            # Card 1: Saldo (Gestão)
            with ui.card().classes("flex-1 p-5"):
                ui.label("Saldo Disponível").classes("text-sm text-slate-500")
                ui.label("R$ 0,00").classes("text-3xl font-bold text-slate-800 my-2")
                ui.label("Aguardando integração da rota /accounts/me no Gateway").classes("text-xs text-slate-400")

            # Card 2: Nova Transferência (Transferências)
            with ui.card().classes("flex-1 p-5"):
                ui.label("Nova Transferência").classes("text-lg font-semibold mb-2")
                ui.select(options={}, label="Destinatário (Vínculos ativos)").classes("w-full mb-2")
                ui.number("Valor (R$)", min=0.01, format="%.2f").classes("w-full mb-3")
                ui.button("Transferir", icon="send").classes("w-full bg-blue-600 text-white").props("disable")

        # Seção Inferior: Vínculos e Notificações
        with ui.row().classes("w-full gap-6"):
            with ui.card().classes("flex-1 p-5"):
                ui.label("Meus Vínculos").classes("text-lg font-semibold mb-2")
                ui.label("Aguardando integração do serviço de Vínculos.").classes("text-sm text-slate-500")

            with ui.card().classes("flex-1 p-5"):
                ui.label("Notificações em Tempo Real").classes("text-lg font-semibold mb-2")
                ui.label("Aguardando eventos do serviço de Notificações...").classes("text-xs text-slate-400")

    async def validate_session():
        try:
            me = await client.get_me()
            user_label.set_text(f"{me.get('name')} ({me.get('email')})")
        except httpx.HTTPStatusError:
            ui.notify("Sessão expirada. Faça login novamente.", type="warning")
            logout()
        except Exception:
            pass

    ui.timer(0.1, validate_session, once=True)