
import customtkinter as ctk


class MyProgressBar(ctk.CTkProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create the text item in the internal canvas
        self._canvas.create_text(0, 0, text="", fill="yellow",
                                 font=('Arial', 10), anchor="c", tags="progress_text")

    # override function to move the progress text at the center of the internal canvas
    def _update_dimensions_event(self, event):
        super()._update_dimensions_event(event)
        self._canvas.coords("progress_text", event.width/2, event.height/2)

    # override function to update the progress text whenever new value is set
    def set(self, val, **kwargs):
        super().set(val, **kwargs)
        self._canvas.itemconfigure("progress_text", text=int(val*100))

    def set_with_text(self, val, text):
        super().set(val)
        self._canvas.itemconfigure("progress_text", text=text)
        