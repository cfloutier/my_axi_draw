
import customtkinter as ctk


class MyProgressBar(ctk.CTkProgressBar):
    def __init__(self, master, font_size = 12, text_color="white", *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.font = ("Arial", font_size)


        # create the text item in the internal canvas
        self.text_id = self._canvas.create_text(0, 0, text="", fill=text_color,
                                 font=('Arial', 10), anchor="c", tags="progress_text")

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)
        # self._canvas.configure(width=self._apply_widget_scaling(self._desired_width), height=self._apply_widget_scaling(self._desired_height))
        
        font_size = self._apply_widget_scaling(self.font[1])
        # self._canvas.configure("progress_text", 
        self._canvas.itemconfig(self.text_id, font=(self.font[0], int(font_size)))

    # override function to move the progress text at the center of the internal canvas
    def _update_dimensions_event(self, event):
        super()._update_dimensions_event(event)
        self._canvas.coords("progress_text", event.width/2, event.height/2)
        # self._canvas._update_dimensions_event(event)
        
    # override function to update the progress text whenever new value is set
    def set(self, val, **kwargs):
        super().set(val, **kwargs)
        self._canvas.itemconfigure("progress_text", text=int(val*100))

    def set_with_text(self, val, text):
        super().set(val)
        self._canvas.itemconfigure("progress_text", text=text)
        