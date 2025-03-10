from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from models import db, Reminder, User
from firebase_service import send_push_notification

def check_reminders(app):
    with app.app_context():
        now = datetime.utcnow().time()
        # Získaj všetky aktívne pripomienky
        reminders = Reminder.query.filter_by(active=True).all()

        for reminder in reminders:
            reminder_time = reminder.reminder_time
            # Over, či je aktuálny čas v rozmedzí 60 sekúnd od nastaveného času pripomienky
            time_diff = datetime.combine(datetime.utcnow().date(), reminder_time) - datetime.utcnow()

            if abs(time_diff.total_seconds()) < 60:
                user = reminder.user

                if user.device_token:
                    try:
                        title = f"Pripomienka: {reminder.title}"
                        body = f"Nezabudni na: {reminder.title}!"
                        # Zavolaj funkciu na odoslanie push notifikácie
                        response = send_push_notification(
                            token=user.device_token,
                            title=title,
                            body=body
                        )
                        # Ulož čas posledného odoslania (napr. ak nechceš posielať opakovane)
                        reminder.last_sent = datetime.utcnow()
                        db.session.commit()

                        print(f"Push notifikácia odoslaná pre {user.email} - {reminder.title}")
                    except Exception as e:
                        print(f"Chyba pri odosielaní push notifikácie: {e}")
                else:
                    print(f"Používateľ {user.email} nemá nastavený device_token, notifikácia neodoslaná.")

def init_scheduler(app):
    # Inicializuj a spusti APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: check_reminders(app),
        trigger="interval",
        seconds=60
    )
    scheduler.start()
    print("Scheduler pre push notifikácie spustený.")
