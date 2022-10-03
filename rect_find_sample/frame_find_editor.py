# import tkinter

# version = tkinter.Tcl().eval('info patchlevel')
# window = tkinter.Tk()
# window.geometry("1200x1000")
# window.title("Editor")

# img = tkinter.PhotoImage(file="result.png")
# canvas = tkinter.Canvas(window, bg="#deb887", height=1200, width=1000)
# canvas.place(x=0, y=0)
# canvas.create_image(0, 0, image=img, anchor=tkinter.NW)

# window.mainloop()

import tkinter
import tkinter.ttk


class Application(tkinter.Frame):

    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 600

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("tkinter canvas trial")
        self.pack()
        self.create_widgets()
        self.startup()

    def create_widgets(self):
        self.start_x = tkinter.StringVar()
        self.start_y = tkinter.StringVar()
        self.current_x = tkinter.StringVar()
        self.current_y = tkinter.StringVar()

        self.label_description = tkinter.ttk.Label(self, text="Mouse position")
        self.label_description.grid(row=0, column=1)
        self.label_start_x = tkinter.ttk.Label(self, textvariable=self.start_x)
        self.label_start_x.grid(row=1, column=1)
        self.label_start_y = tkinter.ttk.Label(self, textvariable=self.start_y)
        self.label_start_y.grid(row=2, column=1)
        self.label_current_x = tkinter.ttk.Label(self, textvariable=self.current_x)
        self.label_current_x.grid(row=3, column=1)
        self.label_current_y = tkinter.ttk.Label(self, textvariable=self.current_y)
        self.label_current_y.grid(row=4, column=1)

        self.test_canvas = tkinter.Canvas(
            self,
            bg="lightblue",
            width=self.CANVAS_WIDTH + 1,
            height=self.CANVAS_HEIGHT + 1,
            highlightthickness=0,
        )
        self.test_canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
        self.test_canvas.bind("<ButtonPress-1>", self.start_pickup)
        self.test_canvas.bind("<B1-Motion>", self.pickup_position)

    def startup(self):
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect = None

    def start_pickup(self, event):
        if 0 <= event.x <= self.CANVAS_WIDTH and 0 <= event.y <= self.CANVAS_HEIGHT:
            self.start_x.set("x : " + str(event.x))
            self.start_y.set("y : " + str(event.y))
            self.rect_start_x = event.x
            self.rect_start_y = event.y

    def pickup_position(self, event):
        if 0 <= event.x <= self.CANVAS_WIDTH and 0 <= event.y <= self.CANVAS_HEIGHT:
            self.current_x.set("x : " + str(event.x))
            self.current_y.set("y : " + str(event.y))
            if self.rect:
                self.test_canvas.coords(
                    self.rect,
                    min(self.rect_start_x, event.x),
                    min(self.rect_start_y, event.y),
                    max(self.rect_start_x, event.x),
                    max(self.rect_start_y, event.y),
                )
            else:
                self.rect = self.test_canvas.create_rectangle(
                    self.rect_start_x,
                    self.rect_start_y,
                    event.x,
                    event.y,
                    outline="red",
                )


root = tkinter.Tk()
app = Application(master=root)
app.mainloop()
