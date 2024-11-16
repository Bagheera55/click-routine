from tkinter import *


class Application():
    def __init__(self, master):
        self.master = master
        self.pressX = None
        self.pressY = None
        self.xyPos = None

        self.master_screen = Toplevel(rootP)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)

        self.createScreenCanvas()

    def createScreenCanvas(self):
        self.master_screen.deiconify()
        rootP.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="top_left_arrow", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)
        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)

        self.master_screen.attributes('-fullscreen', True)

        self.master_screen.attributes('-alpha', .8)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_press(self, event):
        # save mouse drag start position
        self.pressX = self.screenCanvas.canvasx(event.x)
        self.pressY = self.screenCanvas.canvasy(event.y)
        self.xyPos = str(int(self.pressX))+","+str(int(self.pressY))
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        rootP.quit()


def main():
    # will be called from main.py
    global rootP
    rootP = Tk()
    screen = Application(rootP)
    rootP.mainloop()
    return screen.xyPos

if __name__ == '__main__':
    # debug run
    main()
