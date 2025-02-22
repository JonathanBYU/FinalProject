# Press esc to stop the program because it controls your cursor
# I used a very small model for object detection to be able to run on my cheap laptop
# It isn't very accurate and will probably try to click random images on your screen occasionally

import tkinter as tk
from florr_gui import GUI


if __name__ == '__main__':
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
