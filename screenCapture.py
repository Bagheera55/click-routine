from tkinter import *
import pyautogui
import datetime
import os
import sys

if sys.platform == 'win32':
    try:
        import win32api
    except ImportError:
        win32api = None  # Handle gracefully if win32api isn't available


class ScreenCaptureApp:
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.crossH = None
        self.crossV = None
        self.start_x = self.start_y = None
        self.curX = self.curY = None
        self.file_location = ""

        # Transparent fullscreen window for screen capture
        self.master_screen = Toplevel(master)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background="blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)

        self.create_screen_canvas()

    def take_bounded_screenshot(self, x1, y1, width, height):
        try:
            # Adjust coordinates for multi-monitor setups (Windows only)
            if sys.platform == 'win32' and win32api:
                monitors = win32api.EnumDisplayMonitors()
                x_min = min([mon[2][0] for mon in monitors])
                y_min = min([mon[2][1] for mon in monitors])
                x1 -= x_min
                y1 -= y_min

            # Capture the selected region
            im = pyautogui.screenshot(region=(x1, y1, width, height))

            # Save the screenshot
            x = datetime.datetime.now()
            fileName = x.strftime("%H%M%S%f")
            self.file_location = "captures\\" + fileName + ".png"
            self.file_location = self.file_location
            im.save(os.environ['APPDATA'] + "\\ClickRoutine\\" + self.file_location)

            print(f"Screenshot saved: {self.file_location}")
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
        finally:
            self.exit_application()

    def create_screen_canvas(self):
        """Creates a fullscreen canvas for selecting the screenshot area."""
        self.master_screen.deiconify()
        self.master.withdraw()

        self.screen_canvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screen_canvas.pack(fill=BOTH, expand=YES)

        # Bind mouse events
        self.screen_canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screen_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.screen_canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Make the window fullscreen and semi-transparent
        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', 0.8)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_press(self, event):
        """Handles the start of the drag to select a screenshot area."""
        self.start_x = self.screen_canvas.canvasx(event.x)
        self.start_y = self.screen_canvas.canvasy(event.y)
        self.rect = self.screen_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                        outline='gray', width=2, fill="blue")
        self.crossH = self.screen_canvas.create_line(0, 0, 0, 0, width=1, fill="black")
        self.crossV = self.screen_canvas.create_line(0, 0, 0, 0, width=1, fill="black")

    def on_mouse_drag(self, event):
        """Updates the selection rectangle and crosshair while dragging."""
        self.curX, self.curY = event.x, event.y
        self.screen_canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

        # Update crosshair lines
        self.screen_canvas.coords(self.crossH,
                                  self.start_x + ((self.curX - self.start_x) / 4),
                                  self.start_y + ((self.curY - self.start_y) / 2),
                                  self.curX - ((self.curX - self.start_x) / 4),
                                  self.start_y + ((self.curY - self.start_y) / 2))
        self.screen_canvas.coords(self.crossV,
                                  self.start_x + ((self.curX - self.start_x) / 2),
                                  self.start_y + ((self.curY - self.start_y) / 4),
                                  self.start_x + ((self.curX - self.start_x) / 2),
                                  self.curY - ((self.curY - self.start_y) / 4))

    def on_button_release(self, event):
        """Handles the end of the drag and captures the selected region."""
        if self.start_x and self.start_y and self.curX and self.curY:
            x1 = min(self.start_x, self.curX)
            y1 = min(self.start_y, self.curY)
            width = abs(self.curX - self.start_x)
            height = abs(self.curY - self.start_y)
            self.exit_screenshot_mode()
            self.take_bounded_screenshot(x1, y1, width, height)

    def exit_screenshot_mode(self):
        """Closes the screenshot selection window."""
        self.screen_canvas.destroy()
        self.master_screen.withdraw()

    def exit_application(self):
        """Exits the application."""
        self.master.quit()


def main():
    global root
    root = Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()
    return app.file_location


if __name__ == '__main__':
    main()
