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
    
    def filter_tasks(self, keyword=None, category=None, priority=None, status=None):
        """过滤任务"""
        filtered_tasks = self.tasks
        
        # 关键词搜索（在标题和描述中搜索）
        if keyword:
            filtered_tasks = [
                task for task in filtered_tasks 
                if keyword in task["title"].lower() or 
                   keyword in task.get("description", "").lower()
            ]
        
        # 分类过滤
        if category:
            filtered_tasks = [task for task in filtered_tasks if task["category"] == category]
        
        # 优先级过滤
        if priority:
            filtered_tasks = [task for task in filtered_tasks if task["priority"] == priority]
        
        # 状态过滤
        if status:
            filtered_tasks = [task for task in filtered_tasks if task["status"] == status]
        
        return filtered_tasks
    
    def get_task_statistics(self):
        """获取任务统计信息"""
        stats = {
            "total_tasks": len(self.tasks),
            "by_category": {},
            "by_priority": {},
            "by_status": {}
        }
        
        # 按分类统计
        categories = ["工作", "学习", "生活", "其他"]
        for category in categories:
            count = len([task for task in self.tasks if task["category"] == category])
            stats["by_category"][category] = count
        
        # 按优先级统计
        priorities = ["高", "中", "低"]
        for priority in priorities:
            count = len([task for task in self.tasks if task["priority"] == priority])
            stats["by_priority"][priority] = count
        
        # 按状态统计
        statuses = ["未开始", "进行中", "已完成"]
        for status in statuses:
            count = len([task for task in self.tasks if task["status"] == status])
            stats["by_status"][status] = count
        
        return stats
    
    def search_tasks(self, keyword):
        """搜索任务（标题和描述）"""
        keyword = keyword.lower()
        return [
            task for task in self.tasks 
            if keyword in task["title"].lower() or 
               keyword in task.get("description", "").lower()
        ]