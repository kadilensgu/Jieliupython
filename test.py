import os
import json


class ConfigEditor:
    def __init__(self, filename="reqable-rewrites.config.json"):
        self.filename = filename
        self.filepath = os.path.join(os.path.dirname(__file__), self.filename)

    def load(self):
        """安全加载配置"""
        if not os.path.isfile(self.filepath):
            print(f"❌ 文件不存在：{self.filepath}")
            return None
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 加载失败：{e}")
            return None

    def save(self, data):
        """美化写入（缩进 2，中文不转义）"""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 已保存到 {self.filepath}")
        except Exception as e:
            print(f"❌ 保存失败：{e}")

    def find_item_by_name(self, data, item_name):
        """根据 item.name 查找第一个匹配项，返回 (rule_index, item_index, item)"""
        for i, rule in enumerate(data):
            items = rule.get("items", [])
            for j, item in enumerate(items):
                if item.get("name") == item_name:
                    return i, j, item
        return None, None, None

    def update_payload_field(self, item_name: str, field: str, value):
        """
        修改指定 item 的 payload 中的某个字段（支持嵌套，如 'result.mallCwFFlStats.cwShpIntmRatePredIncr'）
        ✅ 自动解析 payload 字符串为 dict → 修改 → 转回格式化 JSON 字符串
        """
        data = self.load()
        if not data:
            return False

        rule_i, item_i, item = self.find_item_by_name(data, item_name)
        if item is None:
            print(f"⚠️  未找到 name = '{item_name}' 的规则项")
            return False

        # 🔍 解析 payload
        payload_str = item.get("action", {}).get("body", {}).get("payload", "")
        if not isinstance(payload_str, str) or not payload_str.strip():
            print(f"⚠️  '{item_name}' 的 payload 为空或非字符串")
            return False

        try:
            payload_dict = json.loads(payload_str)
        except json.JSONDecodeError as e:
            print(f"⚠️  '{item_name}' 的 payload JSON 格式错误：{e}")
            return False

        # 🛠️ 按点号路径设置字段（例如 'result.mallCwFFlStats.cwShpIntmRatePredIncr'）
        keys = field.split(".")
        target = payload_dict
        for k in keys[:-1]:
            if not isinstance(target, dict) or k not in target:
                print(f"⚠️  字段路径 '{field}' 不存在（在 '{k}' 处中断）")
                return False
            target = target[k]
        final_key = keys[-1]
        target[final_key] = value

        # 💾 写回 payload（保持换行缩进美观）
        item["action"]["body"]["payload"] = json.dumps(payload_dict, ensure_ascii=False, indent=2)

        # ✅ 保存
        self.save(data)
        print(f"✅ 已更新 '{item_name}' → `{field}` = {value}")
        return True


# ✨ 示例调用（你可以替换成你前端传来的参数）
if __name__ == "__main__":
    editor = ConfigEditor()

    # 👇 前端传来：想改“美国数据面板”里的 cwShpIntmRatePredIncr 为 0.55
    editor.update_payload_field(item_name="美国数据面板", field="result.mallCwFFlStats.cwShpIntmRatePredIncr", value=0.55)

    # 👇 其他例子：
    # editor.update_payload_field("全球统计", "result.mallSaleInfo.todaySaleNum", 999999)
    # editor.update_payload_field("全球商品上新状态", "result.productSkcStatusAggregation.0.count", 888888)
