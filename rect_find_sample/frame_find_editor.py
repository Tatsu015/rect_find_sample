import tkinter

version = tkinter.Tcl().eval('info patchlevel')
window = tkinter.Tk()
window.geometry("400x300")
window.title("Editor")

# キャンバス作成
canvas = tkinter.Canvas(window, bg="#deb887", height=200, width=200)
# キャンバス表示
canvas.place(x=0, y=0)
 
# イメージ作成
img = tkinter.PhotoImage(file="result.jpeg", width=200, height=200)
# キャンバスにイメージを表示
canvas.create_image(30, 30, image=img, anchor=tkinter.NW)
 
window.mainloop()