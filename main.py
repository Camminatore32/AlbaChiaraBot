# 👉 ALBACCHIARA BOT - Tutto in un file (main.py)

import os
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# === TOKEN ENV VARIABLE ===
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ ERRORE: Devi aggiungere la variabile BOT_TOKEN nelle Secrets di Replit.")
    exit()

# === MEMORIA UTENTE ===
user_data = {}

# === MENU DATA ===
MENU_BIBITE = {
    "Acqua": [
        ("Acqua naturale 100cl", "€ 3"),
        ("Acqua frizzante 100cl", "€ 3"),
        ("Acqua naturale 50cl", "€ 1,50"),
        ("Acqua frizzante 50cl", "€ 1,50")
    ],
    "Bibite": [
        ("Coca-Cola 25cl", "€ 3"),
        ("Coca-Cola Zero 25cl", "€ 3"),
        ("Fanta 25cl", "€ 3"),
        ("Schweppes Tonica 18cl", "€ 3"),
        ("Chinotto 20cl", "€ 3"),
        ("Estathè 33cl", "€ 3"),
        ("Gazzosa 33cl", "€ 2")
    ],
    "Caffè": [
        ("Espresso", "€ 1,50"),
        ("Cappuccino", "€ 3"),
        ("Americano", "€ 3"),
        ("Caffè d'orzo", "€ 2"),
        ("Ginseng", "€ 2")
    ],
    "Soft Drinks": [
        ("Crodino", "€ 4"),
        ("Campari Soda", "€ 4"),
        ("Succo di frutta", "€ 3")
    ],
    "Birra": [
        ("Tennent's", "€ 5"),
        ("Beck's 33cl", "€ 4"),
        ("Heineken 33cl", "€ 4"),
        ("Messina Cristalli di Sale 33cl", "€ 5"),
        ("Corona 33cl", "€ 5"),
        ("Ceres 33cl", "€ 5"),
        ("Moretti 33cl", "€ 4")
    ],
    "Vini Bianchi": [
        ("LAGUNA SECCA - Chardonnay", "€ 20"),
        ("COSTADUNE - Grillo", "€ 20"),
        ("INZOLIA - Cantine Paolini", "€ 15"),
        ("VERDELICIA - Chardonnay Bio", "€ 20"),
        ("MARIA COSTANZA - Inzolia, Chardonnay", "€ 35")
    ],
    "Vini Rossi": [
        ("PASSO DI LUNA - Sirah, Merlot, Nero d'Avola", "€ 20"),
        ("COSTADUNE - Nero d'Avola", "€ 20"),
        ("NERO D'AVOLA - Cantine Paolini", "€ 15"),
        ("MARIA COSTANZA - Nero d'Avola", "€ 40")
    ],
    "Cocktails": [
        ("APEROL SPRITZ", "€ 8"),
        ("GIN TONIC BOMBAY", "€ 8"),
        ("MOJITO", "€ 8"),
        ("NEGRONI", "€ 8"),
        ("PINA COLADA", "€ 8"),
        ("CAMPARI SPRITZ", "€ 8")
    ]
}

MENU_PASTI = {
    "Happy Hour": [
        ("Aperitivo Rinforzato (18:00-20:00)", "€ 15")
    ],
    "Tavola Calda": [
        ("Composizione Arancini Mignon", "€ 15"),
        ("Arancine Speciali", "€ 6"),
        ("Arancine (Ragù/Pomodoro)", "€ 3"),
        ("Mignolate", "€ 3"),
        ("Pizzette", "€ 3")
    ],
    "Stuzzicheria": [
        ("Tagliere Salumi e Formaggi", "€ 17"),
        ("Patatine Fritte", "€ 5"),
        ("Panelle", "€ 5"),
        ("Bruschettone", "€ 4")
    ],
    "Insalatone": [
        ("Insalata della Casa", "€ 11"),
        ("Insalata di Tonno", "€ 11"),
        ("Insalatona di Pollo", "€ 11"),
        ("Insalata di Mare", "€ 16"),
        ("Cous Cous di Verdure", "€ 11"),
        ("Caprese", "€ 11")
    ],
    "Panini & Piadine": [
        ("Piccante", "€ 6"),
        ("Contadino", "€ 6"),
        ("Ricco", "€ 7"),
        ("Albachiara", "€ 7")
    ],
    "Toast": [
        ("Semplice", "€ 5"),
        ("Tonno Subito", "€ 6"),
        ("Matto", "€ 6"),
        ("Salame e Provola", "€ 5"),
        ("Prosciutto e Provola", "€ 5")
    ],
    "Primi": [
        ("Pasta a Forno del Giorno", "€ 7"),
        ("Lasagne del Giorno", "€ 7"),
        ("Cous Cous di Mare", "€ 20"),
        ("Cous Cous di Terra", "€ 11")
    ],
    "Dessert": [
        ("Macedonia di Frutta", "€ 5"),
        ("Tiramisu", "€ 7"),
        ("Semifreddo Ricotta e Pistacchio", "€ 7"),
        ("Cioccolato 7 Veli", "€ 7")
    ],
    "Gelati e Granite": [
        ("Granita (Limone/Fragola/Coca Cola/Menta)", "€ 3"),
        ("Cremino al Caffè", "€ 3"),
        ("Gelati (Vedi Tabellone)", "Vari prezzi")
    ]
}

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"fase": "scelta_posizione", "ordine": {}}
    keyboard = [
        [InlineKeyboardButton("🟡 Ombrellone", callback_data='ombrellone')],
        [InlineKeyboardButton("🪑 Tavolo", callback_data='tavolo')]
    ]
    await update.message.reply_text(
        "🌊 *Benvenuto nel modulo ordine di Albachiara!*\nScegli tra le seguenti opzioni:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# === GESTIONE BOTTONI ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data in ["ombrellone", "tavolo"]:
        user_data[user_id]["tipo"] = data
        user_data[user_id]["fase"] = "scelta_numero"
        await mostra_numeri(query, data)

    elif data.startswith("num_"):
        # Gestione selezione numero ombrellone/tavolo
        numero = int(data.split("_")[1])
        if user_id not in user_data:
            user_data[user_id] = {"fase": "menu_ordini", "ordine": {}}
        user_data[user_id]["numero"] = numero
        user_data[user_id]["fase"] = "menu_ordini"
        await query.edit_message_text(
            f"✅ Selezionato: *{user_data[user_id]['tipo'].title()} n°{numero}*",
            parse_mode="Markdown"
        )
        await mostra_menu_ordini(query, user_id)

    elif data in ["bibite", "pasti"]:
        if user_id not in user_data:
            user_data[user_id] = {"fase": data, "ordine": {}}
        user_data[user_id]["fase"] = data
        if data == "bibite":
            await mostra_menu_bibite(query)
        else:
            await mostra_menu_pasti(query)
    
    elif data.startswith("categoria_"):
        # Gestione selezione categoria menu
        categoria = data.split("_", 1)[1]
        await mostra_items_categoria(query, categoria)
    
    elif data.startswith("item_"):
        # Gestione selezione item specifico
        item_data = data.split("_", 1)[1]
        await gestisci_selezione_item(query, user_id, item_data)
    
    elif data == "torna_menu":
        if user_id not in user_data:
            user_data[user_id] = {"fase": "menu_ordini", "ordine": {}}
        await mostra_menu_ordini(query, user_id)
    
    elif data == "inserisci_libero":
        if user_id not in user_data:
            user_data[user_id] = {"fase": "inserimento_libero", "ordine": {}}
        user_data[user_id]["fase"] = "inserimento_libero"
        await query.edit_message_text("✍️ Scrivi il tuo ordine personalizzato:")

    elif data == "conferma":
        u = user_data[user_id]
        riepilogo = f"🧾 *Riepilogo Ordine*\n📍 {u['tipo'].title()} n°{u['numero']}\n\n"
        
        # Gestisci il nuovo formato degli ordini
        ordine = u.get('ordine', {})
        
        # Bibite
        if 'bibite' in ordine:
            if isinstance(ordine['bibite'], list):
                riepilogo += "🥤 *Bibite:*\n"
                for item in ordine['bibite']:
                    riepilogo += f"• {item}\n"
            else:
                riepilogo += f"🥤 *Bibite:* {ordine['bibite']}\n"
        
        # Pasti
        if 'pasti' in ordine:
            if isinstance(ordine['pasti'], list):
                riepilogo += "🍽️ *Pasti:*\n"
                for item in ordine['pasti']:
                    riepilogo += f"• {item}\n"
            else:
                riepilogo += f"🍽️ *Pasti:* {ordine['pasti']}\n"
        
        # Ordine personalizzato
        if 'personalizzato' in ordine:
            riepilogo += f"✍️ *Personalizzato:* {ordine['personalizzato']}\n"
        
        if not any(key in ordine for key in ['bibite', 'pasti', 'personalizzato']):
            riepilogo += "❌ Nessun ordine inserito"
        
        # Crea il messaggio per WhatsApp (senza markdown)
        whatsapp_msg = riepilogo.replace("*", "").replace("🧾", "").replace("📍", "").replace("🥤", "").replace("🍽️", "").replace("✍️", "")
        whatsapp_msg = whatsapp_msg.replace("•", "-")
        
        # Encode per URL
        import urllib.parse
        encoded_msg = urllib.parse.quote(whatsapp_msg)
        
        # Crea il link WhatsApp che invia automaticamente
        whatsapp_link = f"https://wa.me/393716681304?text={encoded_msg}"
        
        # Mostra il riepilogo e il pulsante per inviare
        keyboard = [
            [InlineKeyboardButton("📲 Invia Ordine su WhatsApp", url=whatsapp_link)],
            [InlineKeyboardButton("🔙 Modifica Ordine", callback_data="torna_menu")]
        ]
        
        await query.edit_message_text(
            riepilogo, 
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# === MESSAGGI ===
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    fase = user_data.get(user_id, {}).get("fase")

    if fase in ["bibite", "pasti"]:
        user_data[user_id]["ordine"][fase] = text
        user_data[user_id]["fase"] = "menu_ordini"
        await mostra_menu(update, context)
    
    elif fase == "inserimento_libero":
        user_data[user_id]["ordine"]["personalizzato"] = text
        user_data[user_id]["fase"] = "menu_ordini"
        await update.message.reply_text("✅ Ordine personalizzato aggiunto!")
        await mostra_menu(update, context)

# === MOSTRA NUMERI OMBRELLONE/TAVOLO ===
async def mostra_numeri(query, tipo):
    if tipo == "ombrellone":
        # Ombrelloni 1-30, disposti in righe da 6
        keyboard = []
        for i in range(0, 30, 6):
            row = []
            for j in range(6):
                if i + j + 1 <= 30:
                    row.append(InlineKeyboardButton(f"{i+j+1}", callback_data=f"num_{i+j+1}"))
            keyboard.append(row)
    else:  # tavolo
        # Tavoli 1-10, disposti in righe da 5
        keyboard = []
        for i in range(0, 10, 5):
            row = []
            for j in range(5):
                if i + j + 1 <= 10:
                    row.append(InlineKeyboardButton(f"{i+j+1}", callback_data=f"num_{i+j+1}"))
            keyboard.append(row)
    
    await query.edit_message_text(
        f"🔢 Seleziona il numero del tuo *{tipo}*:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# === MOSTRA MENU ORDINI ===
async def mostra_menu_ordini(query, user_id):
    keyboard = [
        [InlineKeyboardButton("🥤 Bibite", callback_data="bibite")],
        [InlineKeyboardButton("🍽️ Pasti", callback_data="pasti")],
        [InlineKeyboardButton("✅ Conferma Ordine", callback_data="conferma")]
    ]
    await query.message.reply_text(
        "📋 Seleziona un'opzione:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# === MOSTRA MENU (versione per Update) ===
async def mostra_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🥤 Bibite", callback_data="bibite")],
        [InlineKeyboardButton("🍽️ Pasti", callback_data="pasti")],
        [InlineKeyboardButton("✅ Conferma Ordine", callback_data="conferma")]
    ]
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="📋 Seleziona un'opzione:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# === AVVIO BOT ===
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ AlbachiaraBot avviato!")
    await app.run_polling()

# === MENU FUNCTIONS ===
async def mostra_menu_bibite(query):
    keyboard = []
    for categoria in MENU_BIBITE.keys():
        keyboard.append([InlineKeyboardButton(f"🍹 {categoria}", callback_data=f"categoria_bibite_{categoria}")])
    
    keyboard.append([InlineKeyboardButton("✍️ Inserimento Libero", callback_data="inserisci_libero")])
    keyboard.append([InlineKeyboardButton("🔙 Torna al Menu", callback_data="torna_menu")])
    
    await query.edit_message_text(
        "🍹 *MENU BIBITE*\nScegli una categoria:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def mostra_menu_pasti(query):
    keyboard = []
    for categoria in MENU_PASTI.keys():
        keyboard.append([InlineKeyboardButton(f"🍽️ {categoria}", callback_data=f"categoria_pasti_{categoria}")])
    
    keyboard.append([InlineKeyboardButton("✍️ Inserimento Libero", callback_data="inserisci_libero")])
    keyboard.append([InlineKeyboardButton("🔙 Torna al Menu", callback_data="torna_menu")])
    
    await query.edit_message_text(
        "🍽️ *MENU PASTI*\nScegli una categoria:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def mostra_items_categoria(query, categoria_data):
    tipo, categoria = categoria_data.split("_", 1)
    menu_data = MENU_BIBITE if tipo == "bibite" else MENU_PASTI
    
    if categoria not in menu_data:
        await query.edit_message_text("❌ Categoria non trovata")
        return
    
    keyboard = []
    items = menu_data[categoria]
    
    for item, prezzo in items:
        keyboard.append([InlineKeyboardButton(f"{item} - {prezzo}", callback_data=f"item_{tipo}_{categoria}_{item}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Torna alle Categorie", callback_data=f"{tipo}")])
    
    emoji = "🍹" if tipo == "bibite" else "🍽️"
    await query.edit_message_text(
        f"{emoji} *{categoria.upper()}*\nScegli un prodotto:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def gestisci_selezione_item(query, user_id, item_data):
    parts = item_data.split("_", 2)
    tipo = parts[0]
    categoria = parts[1]
    item = parts[2]
    
    # Aggiungi l'item all'ordine
    if "ordine" not in user_data[user_id]:
        user_data[user_id]["ordine"] = {}
    
    if tipo not in user_data[user_id]["ordine"]:
        user_data[user_id]["ordine"][tipo] = []
    
    user_data[user_id]["ordine"][tipo].append(f"{categoria}: {item}")
    
    await query.edit_message_text(
        f"✅ Aggiunto all'ordine:\n*{categoria}: {item}*\n\nCosa vuoi fare adesso?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Torna al Menu", callback_data="torna_menu")],
            [InlineKeyboardButton("➕ Aggiungi Altro", callback_data=tipo)],
            [InlineKeyboardButton("✅ Conferma Ordine", callback_data="conferma")]
        ])
    )

# === ESECUZIONE ===
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
