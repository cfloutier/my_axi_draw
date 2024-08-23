
main_app = None

def refresh_ui():
    global main_app 
    main_app.refresh_ui()


def my_log(text: str):
    if not main_app:
        return
    main_app.log(text)
    