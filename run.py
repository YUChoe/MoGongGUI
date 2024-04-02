import flet as FT
import requests
import time
import json


def main(page: FT.Page) -> None:
    page.title = 'MoGong API test'
    page.window_width = 820
    page.window_height = 990
    page.vertical_alignment = FT.MainAxisAlignment.CENTER

    txt_number = FT.TextField(value="0", text_align=FT.TextAlign.RIGHT, width=200)
    before_id = FT.TextField(value="null", text_align=FT.TextAlign.RIGHT, width=100)
    after_id = FT.TextField(value="null", text_align=FT.TextAlign.RIGHT, width=100)
    lv = FT.ListView(spacing=1, padding=1, auto_scroll=False)

    def refresh(e):
        print(page.window_width, page.window_height)
        update_time = float(txt_number.value)
        ctime = time.time()
        if ctime < update_time + 10:
            print("not yet", update_time + 10)
            return
        svg_content = """<svg rpl="" fill="currentColor" height="24" icon-name="text-post-outline" viewBox="0 0 20 20" width="24" xmlns="http://www.w3.org/2000/svg">      <path d="M6 13h8v1.25H6V13Zm0-2.75h8V9H6v1.25Zm13-7.625v14.75A1.627 1.627 0 0 1 17.375 19H2.625A1.627 1.627 0 0 1 1 17.375V2.625A1.627 1.627 0 0 1 2.625 1h14.75A1.627 1.627 0 0 1 19 2.625Zm-1.25 0a.375.375 0 0 0-.375-.375H2.625a.375.375 0 0 0-.375.375v14.75a.375.375 0 0 0 .375.375h14.75a.375.375 0 0 0 .375-.375V2.625ZM6 6.25h8V5H6v1.25Z"></path>    </svg>"""

        lv.controls.clear()

        datas = {}
        # datas = json.loads(fetchMoGong("", "", 20))
        datas = json.loads(fetchMoGongTest())
        print(datas["kind"], str(ctime))
        after_id.value = datas["data"]["after"]
        before_id.value = datas["data"]["before"]
        datas = datas["data"]["children"]
        txt_number.value = str(ctime)

        for l in datas:
            ll = l["data"]
            print("*", ll["title"])
            print("  -", ll["url"])

            _avatar = FT.Stack(
                [
                    FT.Image(src="""<svg xmlns="http://www.w3.org/2000/svg" fill="#111111" width=76 height=76 </svg>""", width=76, height=76),
                    FT.Container(
                        content=FT.Image(src=svg_content, width=24, height=24),
                        alignment=FT.alignment.center
                    )

                ],
                width=76, height=76
            )


            if "thumbnail" in ll and ll["thumbnail"] != "self":
                # _avatar = FT.Image(src=ll["thumbnail"], width=ll["thumbnail_width"], height=ll["thumbnail_height"])
                _w = int(ll["thumbnail_width"])
                _h = int(ll["thumbnail_height"])
                print("  -", _w, _h, 76, int(76 * _h / _w))
                _avatar = FT.Image(src=ll["thumbnail"], width=76, height=int(76 * _h / _w))
            _author = FT.Text(ll["author"], color='#FFFFFF', size=10)
            if ll["author_flair_text"]:
                _author = FT.Text(ll["author_flair_text"], bgcolor=ll["author_flair_background_color"], color='#FFFFFF', size=10)
            # _author = FT.Text(ll["author_flair_text"], bgcolor=ll["author_flair_background_color"], color='#FFFFFF', size=10)

            lv.controls.append(
                FT.Row(
                    [
                        _avatar,
                        FT.Container(
                            content=FT.Column(
                                [
                                    FT.Row(
                                        [
                                            FT.Text(ll["link_flair_text"], bgcolor=ll["link_flair_background_color"], color='#FFFFFF', size=10),
                                            _author,
                                            # time
                                        ]
                                    ),
                                    FT.Row([
                                        FT.Text(ll["title"], size=14, weight=FT.FontWeight.BOLD),
                                        # FT.Text(f'{ll["url"]}', size=11)
                                        ]),
                                ],
                                tight=True, spacing=0,
                                # expand=True,
                            ),
                            bgcolor=FT.colors.GREY_800,
                            ink=True,
                            on_click=lambda e: print("Clickable with Ink clicked!"),
                            height =76,
                        ),
                    ],
                ),
            )

        page.update()

    def fetchMoGongTest():
        with open('sample.json') as fp:
            return fp.read()

    def fetchMoGong(after, before, count):
        r = requests.get(f'https://www.reddit.com/r/MoGong/new/.json?limit={count}')
        if r.status_code == 200:
            return r.text
        else:
            return ""

    page.add(
        FT.Row(
            [
                lv,

            ],
            alignment=FT.MainAxisAlignment.CENTER,
        ),
        FT.Row(
            [
                FT.IconButton(FT.icons.REFRESH, on_click=refresh),
                before_id,
                after_id,
                txt_number,
            ],
            alignment=FT.MainAxisAlignment.CENTER,
        )
    )
    refresh(None)  # auto-refresh

FT.app(target=main)