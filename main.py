import webview
from script import Script

# python -m PyInstaller -F --add-data "assets;assets" main.py


class Api:
    def submit_data(self, fromdata):
        S = Script()
        return S.run(fromdata)

    def default_data(self):
        S = Script()
        return S.read_form_default_data()


def create_window():
    api = Api()
    window = webview.create_window(
        #
        "Modify Response Data",
        url="./view/index.html",
        js_api=api,
        width=1200,
        height=800,
        maximized=True,
    )
    webview.start()


if __name__ == "__main__":
    create_window()
