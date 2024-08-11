
main_app = None

def refresh_ui():
    global main_app 
    main_app.refresh_ui()


def my_log(text: str):
    main_app.log(text)
    