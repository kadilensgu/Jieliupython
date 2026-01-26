import re


class Script:

    def __init__(self, name):
        self.name = name
        print(f"已创建。")

    def _update_field(self, formdata):
        config_path = "./reqable-rewrites.config"
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("\\", "_")
        for key, value in formdata.items():
            value = str(value)
            pattern = rf'(_"{key}_"\s*:\s*)([^,\n}}]*)'
            content = re.sub(pattern, lambda m: m.group(1) + value, content)
        content = content.replace("_", "\\")
        print(content)

    def run(self, formdata):
        """运行脚本的主方法"""
        self._update_field(formdata)
