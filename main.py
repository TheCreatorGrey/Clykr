from tkinter import Tk, Label, Label, Button, Frame, OptionMenu, StringVar
from time import sleep

import threading, keyboard
import pydirectinput as pyd


class Clicker:
    def __init__(self):
        pass


    def start(
            self, 
            trigger="e",
            coolDown=0.01,
            mode="Default",
            clickOption="Left"
        ):

        self.trigger = trigger
        self.coolDown = coolDown
        self.mode = mode
        self.clickOption = clickOption

        self.toggle = False
        self.holding = False
    
        self.running = True
        self.thread = threading.Thread(
            target=self.startLoop
        ).start()


    def startLoop(self):
        pyd.PAUSE = self.coolDown

        while self.running:
            pressed = keyboard.is_pressed(self.trigger)

            if self.mode == "Default":
                self.toggle = pressed
            elif self.mode == "Toggle":
                if pressed:
                    if not self.holding:
                        self.toggle = not self.toggle
                        self.holding = True
                else:
                    self.holding = False

            if self.toggle:
                if self.clickOption == "Left":
                    pyd.leftClick()
                elif self.clickOption == "Middle":
                    pyd.middleClick()
                elif self.clickOption == "Right":
                    pyd.rightClick()
            else:
                sleep(0.01)

    
    def stop(self):
        self.running = False



class Interface(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.clicker = Clicker()

        self.config(
            bg="#000000",
            padx=20,
            pady=20
        )

        parent.title("Clykr V2")
        parent.geometry("220x200")

        self.dropdowns = []
        self.labels = []


        self.triggerLabel = Label(self, text="Trigger (s):", bg="#000000", fg="#FEF6E5")
        self.triggerLabel.grid(row=1, column=1)

        self.triggerValue = StringVar(self, "E")
        self.triggerOption = OptionMenu(
            self, 
            self.triggerValue,
            *list("QWERTYUIOPASDFGHJJKZXCVBNM1234567890")
        )
        self.dropdowns.append(self.triggerOption)
        self.triggerOption.grid(row=1, column=2, pady=5)



        self.coolDownLabel = Label(self, text="Cooldown (s):", bg="#000000", fg="#FEF6E5")
        self.coolDownLabel.grid(row=2, column=1)

        self.coolDownValue = StringVar(self, 0.01)
        self.coolDownOption = OptionMenu(
            self, 
            self.coolDownValue,
            *[0.01, 0.05, 0.1, 0.5, 1]
        )
        self.dropdowns.append(self.coolDownOption)
        self.coolDownOption.grid(row=2, column=2, pady=5)



        self.modeLabel = Label(self, text="Mode:", bg="#000000", fg="#FEF6E5")
        self.modeLabel.grid(row=3, column=1)

        self.modeValue = StringVar(self, "Default")
        self.modeOption = OptionMenu(
            self, 
            self.modeValue,
            *["Default",
            "Toggle"])
        self.dropdowns.append(self.modeOption)
        self.modeOption.grid(row=3, column=2, pady=5)



        self.mouseLabel = Label(self, text="Mouse:", bg="#000000", fg="#FEF6E5")
        self.mouseLabel.grid(row=4, column=1)

        self.mouseValue = StringVar(self, "Left")
        self.mouseOption = OptionMenu(
            self, 
            self.mouseValue,
            *["Left",
            "Middle",
            "Right"],
        )
        self.dropdowns.append(self.mouseOption)
        self.mouseOption.grid(row=4, column=2, pady=5)



        for d in self.dropdowns:
            d.config(
                width=8,
                bg="#484848", 
                fg="#FEF6E5",
                activebackground="#8A37D4", 
                activeforeground="#ffffff",
                highlightthickness=0,
                border=0
            )

            menu = d["menu"]
            menu.config(
                bg="#000000", 
                fg="#ffffff", 
                activebackground="#8A37D4", 
                activeforeground="#ffffff"
            )
        

        self.startBtn = Button(self, text="Start", command=self.startClicker)
        self.startBtn.config(
            border=0,
            padx=20,
            bg="#8A37D4",
            fg="#ffffff",
            activebackground="#484848", 
            activeforeground="#ffffff"
        )
        self.startBtn.grid(row=5, column=1, pady=5)

    def startClicker(self):
        self.clicker.start(
            self.triggerValue.get(),
            float(self.coolDownValue.get()),
            self.modeValue.get(),
            self.mouseValue.get()
        )

        self.startBtn.config(
            text="Stop", 
            command=self.stopClicker
        )

    def stopClicker(self):
        self.clicker.stop()
        
        self.startBtn.config(
            text="Start", 
            command=self.startClicker
        )


root = Tk()
root.config(bg="#000000")
root.resizable(width=False, height=False)
root.iconbitmap("icon.ico")

Interface(root).grid(row=1, column=1)
root.mainloop()