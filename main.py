import webview
from script import Script


class Api:
    def submit_data(self, fromdata):
        print(fromdata)
        # 类型
        # script = Script("示例脚本")
        # script.run(fromdata)


def create_window():
    api = Api()
    window = webview.create_window(
        #
        "Modify Response Data",
        url="index.html",
        js_api=api,
        width=800,
        height=600,
    )
    webview.start()


if __name__ == "__main__":
    create_window()
