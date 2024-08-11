from globals import my_log, refresh_ui

from settings import SETTINGS, INTERNAL_SETTINGS
from tools.ctk.base_frame import BaseFrame
import customtkinter as ctk
from pathlib import Path

class SettingsFrame(BaseFrame):

    def __init__(self, master: ctk.CTkFrame, **kwargs):
        super().__init__(master, label=None, **kwargs, width=500)

        self.grid_columnconfigure(0, weight=100)
        self.first_pad_y = 2
        self._padx = 2

        self.col = 1
        self.profile_combo = self.Combo(label="Profile : ", values = self.list_profiles(), command = self.on_profile_changed, inline=True)
        self.profile_combo.set(INTERNAL_SETTINGS.profile_name)
     
        # self.Button("Change Profile", self.load, inline=True)
        self.Button("Save New", self.save, inline=True, width=50)
        self.Button("Reset", self.reset, inline=True, width=50)

    def on_profile_changed(self, profile_name):      

        INTERNAL_SETTINGS.profile_name = profile_name
        INTERNAL_SETTINGS._save()
        SETTINGS.load()
        # reset all pages
        refresh_ui()

        # print(profile_name)

    def list_profiles(self):
        dir_path = Path(__file__).parent / "settings"
        files = []
        for file in dir_path.iterdir():
            # print(file.name)
            if file.stem != "internal":
                files.append(file.stem)

        return files

    def save(self):
        # dialog = ctk.CTkInputDialog(text="set profile name :", title="profile name")

        # new_profile_name = dialog.get_input()
        new_profile_name = self.profile_combo.get()
        if new_profile_name == INTERNAL_SETTINGS.profile_name:
            my_log(f"{new_profile_name} profile already exists")
            return

        INTERNAL_SETTINGS.profile_name = new_profile_name
        INTERNAL_SETTINGS.save()

        SETTINGS.save()

        self.profile_combo.configure(values=self.list_profiles())
        self.profile_combo.set(new_profile_name)

        # print("profile:",new_profile_name )
        pass

    def reset(self):

        SETTINGS.reset()
        # reset all pages
        refresh_ui()
        INTERNAL_SETTINGS.save()
        SETTINGS._save()

    


        