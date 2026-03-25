from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json

# ---------------- CONFIGURAÇÃO ----------------
TOKEN = "8603352965:AAFgLv6f9SwC9jx1dHudyDMG1UInDdRC-GA"  # Coloque aqui o token do seu bot
PIX_CHAVE = "11950952140=FERNADA M SILVAs"  # Coloque aqui sua chave PIX
ARQUIVO_PRODUTOS = "produtos.json"
# ----------------------------------------------

# Função para carregar produtos do estoque
def carregar_produtos():
    try:
        with open(ARQUIVO_PRODUTOS, "r") as f:
            return json.load(f)
    except:
        return []

# Comando /start do bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    produtos = carregar_produtos()
    buttons = []

    for i, p in enumerate(produtos):
        if p["quantidade"] > 0:
            # Se estoque baixo, mostra alerta 🔴
            estoque_alerta = "🔴 Estoque baixo!" if p["quantidade"] <= 3 else ""
            # Emoji de produto 🎁
            buttons.append([InlineKeyboardButton(
                f"🎁 {p['nome']} - R${p['preco']} ({p['quantidade']} disponíveis) {estoque_alerta}", 
                callback_data=str(i)
            )])

    mensagem_boas_vindas = f"""
👋 Olá, {user.first_name}!

💼 Bem-vindo à *MAFIOSO STORE* — sua loja digital confiável.

📌 Escolha abaixo o produto que deseja comprar:
"""
    if buttons:
        await update.message.reply_text(
            mensagem_boas_vindas, 
            reply_markup=InlineKeyboardMarkup(buttons), 
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("❌ Nenhum produto disponível no momento.")

# Quando o usuário clica em um botão
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    produtos = carregar_produtos()
    produto = produtos[int(query.data)]

    if produto["quantidade"] > 0:
        await query.message.reply_text(
            f"💳 PAGAMENTO PIX\n\nProduto: {produto['nome']}\nValor: R${produto['preco']}\nChave PIX: {PIX_CHAVE}"
        )
        # Reduz estoque automaticamente
        produto["quantidade"] -= 1
        with open(ARQUIVO_PRODUTOS, "w") as f:
            json.dump(produtos, f)
    else:
        await query.message.reply_text("❌ Produto esgotado!")

# Criando o bot e adicionando handlers
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("✅ BOT ONLINE!")
app.run_polling()