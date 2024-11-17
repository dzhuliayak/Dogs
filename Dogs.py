from tkinter import*
from  tkinter import ttk
from tkinter import messagebox as mb
import requests
from PIL import Image, ImageTk
from io import BytesIO


def get_dog_image():
    try:
        response=requests.get("https://dog.ceo/api/breeds/image/random")# функция response будет JSON
        response.raise_for_status()
        data=response.json()
        return data["message"]#message отражается на сайте с которого мы взяли ссылку
    except Exception as e:
        mb.showerror("ошибка", f"возникла ошибка {e} при запросе к API")
        return None

def show_image():
    image_url=get_dog_image()
    if image_url:
        try:
            response=requests.get(image_url, stream=True)
            response.raise_for_status()
            img_data=BytesIO(response.content)
            img=Image.open(img_data)
            img_size=(int(width_spinbox.get()), int(height_spinbox.get()))
            img.thumbnail(img_size)# через запятую, т.к. это кортеж
            img=ImageTk.PhotoImage(img)
            #new_window=Toplevel(window)
            #new_window.title("случайное изображение")
            tab = ttk.Frame(notebook)# типо закладки
            notebook.add(tab, text=f"картинка № {notebook.index("end")+1}")
            lb=ttk.Label(tab, image=img)
            lb.pack(padx=10, pady=10)
            lb.image=img
        except Exception as e:
            mb.showerror("ошибка", f"возникла ошибка {e} при загрузке изображения")
    progress.stop()


def prog():
    progress["value"]=0
    progress.start(30)
    window.after(3000, show_image())

window=Tk()
window.title("картинки с собачкой")
window.geometry("360x420")

label=ttk.Label()
label.pack(pady=10)

button=ttk.Button(text="загрузить изображение", command=prog)
button.pack(pady=10)

progress=ttk.Progressbar(mode="determinate", length=300)
progress.pack(pady=10)

width_label=ttk.Label(text="ширина")
width_label.pack(side="left", pady=(10,0))
width_spinbox=ttk.Spinbox(from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side="left", pady=(0,10))

height_label=ttk.Label(text="высота:")
height_label.pack(side="left", pady=(10,0))
height_spinbox=ttk.Spinbox(from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side="left", pady=(0,10))

top_level_window=Toplevel(window)
top_level_window.title("изображение собачек")

notebook=ttk.Notebook(top_level_window)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

window.mainloop()
