import json
import os
from datetime import datetime

class DataManager:
    def __init__(self, data_file="tasks.json"):
        self.data_file = data_file
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """确保数据文件存在，不存在则创建空文件"""
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def load_tasks(self):
        """加载所有任务数据"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_tasks(self, tasks):
        """保存任务数据到文件"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    def generate_task_id(self):
        """生成唯一任务ID"""
        return str(int(datetime.now().timestamp() * 1000))  # 使用毫秒级时间戳确保唯一性
