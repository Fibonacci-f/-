from data.data_manager import DataManager
from datetime import datetime, timedelta

class TaskService:
    def __init__(self):
        self.data_manager = DataManager()
        self.tasks = self.data_manager.load_tasks()
    
    def get_all_tasks(self):
        """获取所有任务"""
        return self.tasks
    
    def add_task(self, task_data):
        """添加新任务"""
        # 生成任务ID和创建时间
        task = {
            "id": self.data_manager.generate_task_id(),
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **task_data
        }
        
        self.tasks.append(task)
        self.data_manager.save_tasks(self.tasks)
        return task
    
    def update_task(self, task_id, updated_data):
        """更新任务信息"""
        for task in self.tasks:
            if task["id"] == task_id:
                task.update(updated_data)
                self.data_manager.save_tasks(self.tasks)
                return True
        return False
    
    def delete_task(self, task_id):
        """删除任务"""
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        
        if len(self.tasks) != original_count:
            self.data_manager.save_tasks(self.tasks)
            return True
        return False
    
    def get_default_due_date(self):
        """获取默认截止日期（明天）"""
        return (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + 
                timedelta(days=1)).strftime("%Y-%m-%d")
