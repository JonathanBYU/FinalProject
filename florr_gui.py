import tkinter as tk
from flower import Flower
import threading
import keyboard
import json
import mss


flower = Flower()

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection Overlay")
        self.root.attributes('-fullscreen',True)
        self.root.wm_attributes("-topmost", True)
        self.root.attributes('-alpha', 1)

        transparent_color = '#000001'
        self.root.config(bg=transparent_color)
        self.root.wm_attributes('-transparentcolor', transparent_color)

        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg=transparent_color, highlightthickness=0)
        self.canvas.pack()

        self.processing = False
        self.image_processing = False
        self.running = True

        self.update()  # Initial call to update method
    
    def update(self):
        if keyboard.is_pressed('esc'):
            self.running = False
            print("Failsafe activated: Exiting...")
            self.root.quit()
        
        self.canvas.delete("all")
        with mss.mss() as sct:
            sct.shot(output="test.jpg")

        # Only run flower.step() if it's not already running
        if not self.processing:
            threading.Thread(target=self.run_flower_step).start()

        try:
            with open('enemy.json') as file:
                enemies = json.load(file)
        except FileNotFoundError:
            enemies = []
        except json.JSONDecodeError:
            print("Enemy file was empty")
            enemies = []

        for enemy in enemies:
            x = enemy[0]
            y = enemy[1]
            width = enemy[2]
            height = enemy[3]
            enemy_name = enemy[4]
            self.canvas.create_rectangle(x-width/2, y-height/2, x+width/2, y+height/2, outline='red', width=2)
            label = self.canvas.create_text(x,y+height/1.5,font=("Arial Bold", 12),fill='white')
            self.canvas.itemconfig(label, text=enemy_name)

        if self.running:
            self.root.after(5, self.update)  # Schedule the next call
    
    def run_flower_step(self):
        self.processing = True
        try:
            flower.step()
        except Exception as e:
            print(f"Error in flower.step(): {e}")
        finally:
            self.processing = False
