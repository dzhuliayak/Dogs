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
            img.thumbnail((300,300))# через запятую, т.к. это кортеж
            img=ImageTk.PhotoImage(img)
            label.config(image=img)
            label.image=img
        except Exception as e:
            mb.showerror("ошибка", f"возникла ошибка {e} при загрузке изображения")
    progress.stop()


def prog():
    progress["value"]=0
    progress.start(30)
    window.after(3000, show_image)




window=Tk()
window.title("картинки с собачкой")
window.geometry("360x420")

label=ttk.Label()
label.pack(pady=10)

button=ttk.Button(text="загрузить изображение", command=prog)
button.pack(pady=10)

progress=ttk.Progressbar(mode="determinate", length=300)
progress.pack(pady=10)

window.mainloop()



