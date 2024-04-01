import flet as FT
import requests
import time


def main(page: FT.Page) -> None:
    page.title = 'MoGong API test'
    page.vertical_alignment = FT.MainAxisAlignment.CENTER

    txt_number = FT.TextField(value="0", text_align=FT.TextAlign.RIGHT, width=100)

    lv = FT.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    def refresh(e):
        update_time = float(txt_number.value)
        ctime = time.time()
        if ctime > update_time + 10:
            r = requests.get('https://www.reddit.com/r/MoGong/new/.json?limit=20')
            txt_number.value = str(ctime)
            if r.status_code == 200:
                with open('sample.json', 'w') as fp:
                    fp.write(r.text)
                # lv.controls.append(ft.Text(f"Line {count}"))
            else:
                print("error")
        page.update()

    page.add(
        FT.Row(
            [
                txt_number,
                FT.IconButton(FT.icons.REFRESH, on_click=refresh),
                lv,

            ],
            alignment=FT.MainAxisAlignment.CENTER,
        )
    )

FT.app(target=main)