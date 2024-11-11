import random
import psycopg2
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
import requests
from io import BytesIO

# Підключення до бд
conn = psycopg2.connect(
    dbname="courseworkdb",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Визначення стану для запиту даних
AGE, EMAIL, COUNTRY, LANGUAGE, PHONE = range(5)

# Функція для автоматичної реєстрації та запиту даних користувача
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    # Перевірка наявності користувача у базі даних
    cursor.execute("SELECT * FROM \"User\" WHERE UserID = %s", (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        # Автоматична реєстрація користувача
        cursor.execute(
            "INSERT INTO \"User\" (UserID, UserName, UserLastName) VALUES (%s, %s, %s)",
            (user_id, first_name, last_name)
        )
        conn.commit()
        await update.message.reply_text("Welcome! You have been automatically registered.")
    else:
        await update.message.reply_text("Welcome back!")

    # Перевірка, чи є всі дані профілю
    cursor.execute("SELECT UserAge, UserMail, UserCountry, UserLanguage, UserPhone FROM \"User\" WHERE UserID = %s", (user_id,))
    user_data = cursor.fetchone()
    
    if not all(user_data):  # Якщо дані профілю неповні
        await update.message.reply_text("Let's complete your profile. Please enter your age:")
        return AGE  # Перехід до запиту віку

    await update.message.reply_text("Your profile is complete. Use /profile to view it.")
    return ConversationHandler.END

# Запит віку
async def set_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    age = update.message.text
    cursor.execute("UPDATE \"User\" SET UserAge = %s WHERE UserID = %s", (age, user_id))
    conn.commit()
    
    await update.message.reply_text("Thank you! Now, please enter your email:")
    return EMAIL

# Запит email
async def set_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    email = update.message.text
    cursor.execute("UPDATE \"User\" SET UserMail = %s WHERE UserID = %s", (email, user_id))
    conn.commit()
    
    await update.message.reply_text("Great! Now, please enter your country:")
    return COUNTRY

# Запит країни
async def set_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    country = update.message.text
    cursor.execute("UPDATE \"User\" SET UserCountry = %s WHERE UserID = %s", (country, user_id))
    conn.commit()
    
    await update.message.reply_text("Thank you! Now, please enter your language:")
    return LANGUAGE

# Запит мови
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    language = update.message.text
    cursor.execute("UPDATE \"User\" SET UserLanguage = %s WHERE UserID = %s", (language, user_id))
    conn.commit()
    
    await update.message.reply_text("Almost done! Please enter your phone number:")
    return PHONE

# Запит номеру телефону
async def set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    phone = update.message.text
    cursor.execute("UPDATE \"User\" SET UserPhone = %s WHERE UserID = %s", (phone, user_id))
    conn.commit()
    
    await update.message.reply_text("Your profile is now complete! Use /profile to view it.")
    return ConversationHandler.END

# Обробка команди скасування
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Profile setup has been canceled.")
    return ConversationHandler.END

# Визначення ConversationHandler для послідовного запиту даних профілю
profile_conversation = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_email)],
        COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_country)],
        LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_phone)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

# Функція перегляду профілю
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    cursor.execute("SELECT UserAge, UserMail, UserCountry, UserLanguage, UserPhone FROM \"User\" WHERE UserID = %s", (user_id,))
    user_data = cursor.fetchone()
    
    if user_data is None:
        await update.message.reply_text("You are not registered! Use /start to register.")
        return
    
    user_age, user_mail, user_country, user_language, user_phone = user_data
    profile_info = f"Age: {user_age}\nEmail: {user_mail}\nCountry: {user_country}\nLanguage: {user_language}\nPhone: {user_phone}"
    
    cursor.execute("""
        SELECT g.GenerName FROM "Genres" g
        JOIN "FavouriteGenres" fg ON g.GenerID = fg.GenerID
        WHERE fg.UserID = %s
    """, (user_id,))
    genres = cursor.fetchall()
    genres_list = ", ".join([genre[0] for genre in genres])
    
    await update.message.reply_text(f"Here is your profile information:\n{profile_info}")
    await update.message.reply_text(f"Favorite Genres: {genres_list if genres_list else 'None'}")
    
    # Кнопка для додавання/зміни улюблених жанрів
    keyboard = [[InlineKeyboardButton("Edit Favorite Genres", callback_data="edit_genres")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)
    
    # Відображення вибраних фільмів
    cursor.execute("""
        SELECT f.FilmID, f.FilmName FROM "Film" f
        JOIN "FavouriteFilms" ff ON f.FilmID = ff.FilmID
        WHERE ff.UserID = %s
    """, (user_id,))
    favorite_films = cursor.fetchall()
    
    if favorite_films:
        await update.message.reply_text("Your favorite films:")
        for film_id, film_name in favorite_films:
            film_keyboard = [
                [InlineKeyboardButton("Remove from Favorites", callback_data=f"remove_film_{film_id}")],
                [InlineKeyboardButton("View Details", callback_data=f"view_film_{film_id}")]
            ]
            film_reply_markup = InlineKeyboardMarkup(film_keyboard)
            await update.message.reply_text(film_name, reply_markup=film_reply_markup)
    else:
        await update.message.reply_text("No favorite films yet.")

# Функція для редагування улюблених жанрів
async def edit_genres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    cursor.execute("SELECT GenerID, GenerName FROM \"Genres\"")
    all_genres = cursor.fetchall()
    
    cursor.execute("SELECT GenerID FROM \"FavouriteGenres\" WHERE UserID = %s", (user_id,))
    user_genres = [genre[0] for genre in cursor.fetchall()]
    
    keyboard = []
    for genre_id, genre_name in all_genres:
        if genre_id in user_genres:
            keyboard.append([InlineKeyboardButton(f"✔️ {genre_name}", callback_data=f"remove_genre_{genre_id}")])
        else:
            keyboard.append([InlineKeyboardButton(f"{genre_name}", callback_data=f"add_genre_{genre_id}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text("Choose your favorite genres:", reply_markup=reply_markup)

# Обробка додавання та видалення жанрів
async def genre_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    if query.data.startswith("add_genre_"):
        genre_id = int(query.data.split("_")[-1])
        cursor.execute("INSERT INTO \"FavouriteGenres\" (UserID, GenerID) VALUES (%s, %s)", (user_id, genre_id))
        conn.commit()
        await edit_genres(update, context)
        
    elif query.data.startswith("remove_genre_"):
        genre_id = int(query.data.split("_")[-1])
        cursor.execute("DELETE FROM \"FavouriteGenres\" WHERE UserID = %s AND GenerID = %s", (user_id, genre_id))
        conn.commit()
        await edit_genres(update, context)

# Функція для додавання фільму до вибраного
async def add_to_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    film_id = int(query.data.split("_")[-1])
    
    cursor.execute("SELECT * FROM \"FavouriteFilms\" WHERE UserID = %s AND FilmID = %s", (user_id, film_id))
    favorite = cursor.fetchone()
    
    if favorite:
        await query.answer("This film is already in your favorites!")
    else:
        cursor.execute("INSERT INTO \"FavouriteFilms\" (UserID, FilmID) VALUES (%s, %s)", (user_id, film_id))
        conn.commit()
        await query.answer("Film added to favorites!")
        await query.message.reply_text("The film has been added to your favorites.")

# Функція для видалення фільму з вибраного
async def remove_from_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    film_id = int(query.data.split("_")[-1])
    
    cursor.execute("DELETE FROM \"FavouriteFilms\" WHERE UserID = %s AND FilmID = %s", (user_id, film_id))
    conn.commit()
    await query.answer("Film removed from favorites!")
    await query.message.reply_text("The film has been removed from your favorites.")

# Функція для відображення деталей фільму з фото, описом та кнопкою для трейлера
async def view_film_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    film_id = int(query.data.split("_")[-1])
    
    cursor.execute("SELECT FilmName, FilmDescription, FilmPicture, FilmTrailer FROM \"Film\" WHERE FilmID = %s", (film_id,))
    film = cursor.fetchone()
    
    if film:
        film_name, film_description, film_picture_url, film_trailer_url = film
        
        # Завантаження зображення
        response = requests.get(film_picture_url)
        photo = BytesIO(response.content)
        
        # Створення кнопки для трейлера
        keyboard = [[InlineKeyboardButton("Watch Trailer", url=film_trailer_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Надсилання фотографії з описом та кнопкою для трейлера
        await query.message.reply_photo(photo=photo, caption=f"{film_name}\n\n{film_description}", reply_markup=reply_markup)
    else:
        await query.message.reply_text("Details for this film are not available.")
    
    await query.answer()

# Функція для пошуку фільму за назвою
async def search_by_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the name of the film you are looking for:")
    return "FILM_NAME"

async def handle_film_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    film_name = update.message.text
    cursor.execute("SELECT FilmID, FilmName FROM \"Film\" WHERE FilmName ILIKE %s", (f"%{film_name}%",))
    films = cursor.fetchall()
    
    if films:
        await update.message.reply_text("Here are the films found:")
        for film_id, film_name in films:
            film_keyboard = [
                [InlineKeyboardButton("Add to Favorites", callback_data=f"add_film_{film_id}")],
                [InlineKeyboardButton("View Details", callback_data=f"view_film_{film_id}")]
            ]
            film_reply_markup = InlineKeyboardMarkup(film_keyboard)
            await update.message.reply_text(film_name, reply_markup=film_reply_markup)
    else:
        await update.message.reply_text("No films found with that name.")

# Функція для пошуку фільму за жанром
async def search_by_genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT GenerID, GenerName FROM \"Genres\"")
    genres = cursor.fetchall()
    
    keyboard = [[InlineKeyboardButton(genre_name, callback_data=f"search_genre_{genre_id}")] for genre_id, genre_name in genres]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a genre:", reply_markup=reply_markup)

# Обробка вибраного жанру для пошуку фільмів
async def handle_genre_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    genre_id = int(query.data.split("_")[-1])
    
    cursor.execute("""
        SELECT f.FilmID, f.FilmName FROM "Film" f
        JOIN "FilmGenres" fg ON f.FilmID = fg.FilmID
        WHERE fg.GenerID = %s
    """, (genre_id,))
    films = cursor.fetchall()
    
    if films:
        await query.edit_message_text("Here are the films found:")
        for film_id, film_name in films:
            film_keyboard = [
                [InlineKeyboardButton("Add to Favorites", callback_data=f"add_film_{film_id}")],
                [InlineKeyboardButton("View Details", callback_data=f"view_film_{film_id}")]
            ]
            film_reply_markup = InlineKeyboardMarkup(film_keyboard)
            await query.message.reply_text(film_name, reply_markup=film_reply_markup)
    else:
        await query.edit_message_text("No films found in this genre.")

# Перехід до випадкового фільму за улюбленими жанрами
async def random_favorite_film(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    cursor.execute("""
        SELECT f.FilmID, f.FilmName FROM "Film" f
        JOIN "FilmGenres" fg ON f.FilmID = fg.FilmID
        JOIN "FavouriteGenres" fg2 ON fg.GenerID = fg2.GenerID
        WHERE fg2.UserID = %s
    """, (user_id,))
    films = cursor.fetchall()
    
    if films:
        film_id, film_name = random.choice(films)
        film_keyboard = [
            [InlineKeyboardButton("Add to Favorites", callback_data=f"add_film_{film_id}")],
            [InlineKeyboardButton("View Details", callback_data=f"view_film_{film_id}")]
        ]
        film_reply_markup = InlineKeyboardMarkup(film_keyboard)
        await update.message.reply_text(f"Here's a random favorite film suggestion:\n{film_name}", reply_markup=film_reply_markup)
    else:
        await update.message.reply_text("No films found in your favorite genres.")

# Налаштування обробників команд та ConversationHandler для заповнення профілю
app = ApplicationBuilder().token("7913000329:AAHiwkBCC15decLbw_ws5H478kAVMgFqpsQ").build()
app.add_handler(profile_conversation)
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("search_by_name", search_by_name))
app.add_handler(CommandHandler("search_by_genre", search_by_genre))
app.add_handler(CommandHandler("random_favorite_film", random_favorite_film))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_film_name))
app.add_handler(CallbackQueryHandler(add_to_favorites, pattern="^add_film_"))
app.add_handler(CallbackQueryHandler(remove_from_favorites, pattern="^remove_film_"))
app.add_handler(CallbackQueryHandler(view_film_details, pattern="^view_film_"))
app.add_handler(CallbackQueryHandler(edit_genres, pattern="edit_genres"))
app.add_handler(CallbackQueryHandler(genre_handler, pattern="^(add_genre_|remove_genre_)"))
app.add_handler(CallbackQueryHandler(handle_genre_selection, pattern="^search_genre_"))

# Запуск бота
app.run_polling(poll_interval=1, timeout=10)

