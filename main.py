from tkinter import Tk, Label, Label, Button, Frame, OptionMenu, StringVar
from time import sleep

import threading
import keyboard
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
                sleep(self.coolDown)

    
    def stop(self):
        self.running = False



class Interface(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.clicker = Clicker()

        parent.title("Clykr V1")
        parent.geometry("220x200")


        self.triggerLabel = Label(self, text="Trigger (s):")
        self.triggerLabel.grid(row=1, column=1)

        self.triggerValue = StringVar(self, "E")

        self.triggerOption = OptionMenu(
            self, 
            self.triggerValue,
            *list("QWERTYUIOPASDFGHJJKZXCVBNM1234567890"))
        self.triggerOption.config(width=8)
        self.triggerOption.grid(row=1, column=2)



        self.coolDownLabel = Label(self, text="Cooldown (s):")
        self.coolDownLabel.grid(row=2, column=1)

        self.coolDownValue = StringVar(self, 0.01)

        self.coolDownOption = OptionMenu(
            self, 
            self.coolDownValue,
            *[0.01,
            0.05,
            0.1,
            0.5,
            1])
        self.coolDownOption.config(width=8)
        self.coolDownOption.grid(row=2, column=2)



        self.modeLabel = Label(self, text="Mode:")
        self.modeLabel.grid(row=3, column=1)

        self.modeValue = StringVar(self, "Default")

        self.modeOption = OptionMenu(
            self, 
            self.modeValue,
            *["Default",
            "Toggle"])
        self.modeOption.config(width=8)
        self.modeOption.grid(row=3, column=2)



        self.mouseLabel = Label(self, text="Mouse:")
        self.mouseLabel.grid(row=4, column=1)

        self.mouseValue = StringVar(self, "Left")

        self.mouseOption = OptionMenu(
            self, 
            self.mouseValue,
            *["Left",
            "Middle",
            "Right"],
        )
        self.mouseOption.config(width=8)
        self.mouseOption.grid(row=4, column=2)



        self.startBtn = Button(self, text="Start", command=self.startClicker)
        self.startBtn.grid(row=5, column=1)

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
Interface(root).grid(row=1, column=1)
root.mainloop()