import json


class Script:

    def __init__(self):
        self.src_file = "reqable-rewrites.config"
        self.dst_file = "reqable-rewrites.config"

    # 主入口：加载配置、更新配置、保存结果
    def run(self, formdata):
        config = self._load_json(self.src_file)
        self._update_config(config, formdata)
        self._save_json(self.dst_file, config)
        return {"status": 1, "info": "修改成功"}

    # ---------- 核心逻辑 ----------

    def _update_config(self, config, formdata):
        for group in config:
            # 区分区域
            if group.get("name") == "美国区域":
                region_data = formdata.get("usData", {})
            elif group.get("name") == "全球区域":
                region_data = formdata.get("glData", {})
            else:
                continue

            items = group.get("items", [])
            # 以 formData 为驱动源
            for key, value in region_data.items():
                for item in items:
                    payload_str = item.get("action", {}).get("body", {}).get("payload")
                    payload = self._parse_payload(payload_str)
                    if not payload:
                        continue

                    result = payload.get("result")
                    if not isinstance(result, dict):
                        continue

                    # 只在“这个接口原本就有该字段”时修改
                    if self._exists_key(result, key):
                        self._recursive_update(result, key, self._cast_value(value))
                        print(f"🔄 更新 '{item.get('name')}' 中的字段 '{key}' → {value}")
                        item["action"]["body"]["payload"] = json.dumps(payload, ensure_ascii=False, indent=2)
                        break  # 关键：这个字段命中一次就停

    # 递归判断指定的 key 是否在数据结构中存在
    def _exists_key(self, data, target_key):
        if isinstance(data, dict):
            for k, v in data.items():
                if k == target_key:
                    return True
                if isinstance(v, (dict, list)) and self._exists_key(v, target_key):
                    return True
        elif isinstance(data, list):
            for item in data:
                if self._exists_key(item, target_key):
                    return True
        return False

    # 递归更新数据中指定 key 的值（前提是该 key 已存在）
    def _recursive_update(self, data, target_key, new_value):
        if isinstance(data, dict):
            for k in data:
                if k == target_key:
                    data[k] = new_value
                else:
                    self._recursive_update(data[k], target_key, new_value)
        elif isinstance(data, list):
            for item in data:
                self._recursive_update(item, target_key, new_value)

    # 解析 JSON 字符串为 Python 对象
    def _parse_payload(self, payload_str):
        if not isinstance(payload_str, str):
            return None
        try:
            return json.loads(payload_str)
        except Exception:
            return None

    # 类型转换：字符串转为整数/浮点数/原值
    def _cast_value(self, value):
        if not isinstance(value, str):
            return value
        v = value.strip()
        if v.isdigit():
            return int(v)
        try:
            return float(v)
        except ValueError:
            return v

    # 从文件读取并解析 JSON 数据
    def _load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # 将数据序列化为 JSON 并写入文件
    def _save_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- 辅助方法：读取默认数据（可选） ----------
    def read_form_default_data(self):
        config = self._load_json(self.dst_file)

        result_data = {"usData": {}, "glData": {}}

        for group in config:
            if group.get("name") == "美国区域":
                target = result_data["usData"]
            elif group.get("name") == "全球区域":
                target = result_data["glData"]
            else:
                continue

            for item in group.get("items", []):
                payload_str = item.get("action", {}).get("body", {}).get("payload")
                payload = self._parse_payload(payload_str)
                if not payload:
                    continue

                result = payload.get("result")
                if not isinstance(result, dict):
                    continue

                self._collect_fields(result, target)

        return result_data

    # 递归收集数据结构中的所有字段和值，构建扁平化的字典（仅叶子节点）
    def _collect_fields(self, data, target):
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    self._collect_fields(v, target)  # 继续深入
                else:
                    # 叶子值：只收集 str/int/float/bool/None，跳过空字符串（可选）
                    if v not in ("", None) or isinstance(v, (int, float, bool)):
                        target.setdefault(k, v)
        elif isinstance(data, list):
            for item in data:
                self._collect_fields(item, target)
