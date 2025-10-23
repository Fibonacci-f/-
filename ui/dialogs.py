import tkinter as tk
from tkinter import ttk, messagebox
from core.task_service import TaskService

class AddTaskDialog(tk.Toplevel):
    def __init__(self, parent, task_service: TaskService):
        super().__init__(parent)
        self.parent = parent
        self.task_service = task_service
        self.title("添加任务")
        self.geometry("600x500")
        self.resizable(True, True)
        self.result = None  # 用于存储对话框结果
        
        self.create_widgets()
    
    def create_widgets(self):
        container = ttk.Frame(self, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # 任务标题
        ttk.Label(container, text="任务标题:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.title_entry = ttk.Entry(container, width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 任务描述
        ttk.Label(container, text="任务描述:").grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)
        self.desc_text = tk.Text(container, width=30, height=5)
        self.desc_text.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 任务分类
        ttk.Label(container, text="任务分类:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(container, textvariable=self.category_var, 
                                      values=["工作", "学习", "生活", "其他"], width=37)
        category_combo.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        category_combo.current(0)
        
        # 优先级
        ttk.Label(container, text="优先级:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(container, textvariable=self.priority_var, 
                                      values=["高", "中", "低"], width=37)
        priority_combo.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        priority_combo.current(1)
        
        # 截止日期
        ttk.Label(container, text="截止日期:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        self.due_date_entry = ttk.Entry(container, width=40)
        self.due_date_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        self.due_date_entry.insert(0, self.task_service.get_default_due_date())
        
        # 任务状态
        ttk.Label(container, text="状态:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(container, textvariable=self.status_var, 
                                   values=["未开始", "进行中", "已完成"], width=37)
        status_combo.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)
        status_combo.current(0)
        
        # 确认按钮
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="确认添加", command=self.confirm, width=20).pack(pady=10)
    
    def confirm(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("错误", "任务标题不能为空！")
            return
        
        task_data = {
            "title": title,
            "description": self.desc_text.get("1.0", tk.END).strip(),
            "category": self.category_var.get(),
            "priority": self.priority_var.get(),
            "status": self.status_var.get(),
            "due_date": self.due_date_entry.get().strip()
        }
        
        self.result = self.task_service.add_task(task_data)
        self.destroy()


class EditTaskDialog(tk.Toplevel):
    def __init__(self, parent, task_service: TaskService, task_id):
        super().__init__(parent)
        self.parent = parent
        self.task_service = task_service
        self.task_id = task_id
        self.task = next((t for t in task_service.get_all_tasks() if t["id"] == task_id), None)
        
        if not self.task:
            messagebox.showerror("错误", "未找到该任务的数据！")
            self.destroy()
            return
        
        self.title("编辑任务")
        self.geometry("600x500")
        self.resizable(True, True)
        
        self.create_widgets()
    
    def create_widgets(self):
        container = ttk.Frame(self, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # 任务标题
        ttk.Label(container, text="任务标题:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.title_entry = ttk.Entry(container, width=40)
        self.title_entry.insert(0, self.task["title"])
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 任务描述
        ttk.Label(container, text="任务描述:").grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)
        self.desc_text = tk.Text(container, width=30, height=5)
        self.desc_text.insert("1.0", self.task.get("description", ""))
        self.desc_text.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 任务分类
        ttk.Label(container, text="任务分类:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.category_var = tk.StringVar(value=self.task["category"])
        category_combo = ttk.Combobox(container, textvariable=self.category_var, 
                                      values=["工作", "学习", "生活", "其他"], width=37)
        category_combo.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 优先级
        ttk.Label(container, text="优先级:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.priority_var = tk.StringVar(value=self.task["priority"])
        priority_combo = ttk.Combobox(container, textvariable=self.priority_var, 
                                      values=["高", "中", "低"], width=37)
        priority_combo.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 截止日期
        ttk.Label(container, text="截止日期:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        self.due_date_entry = ttk.Entry(container, width=40)
        self.due_date_entry.insert(0, self.task["due_date"])
        self.due_date_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 任务状态
        ttk.Label(container, text="状态:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        self.status_var = tk.StringVar(value=self.task["status"])
        status_combo = ttk.Combobox(container, textvariable=self.status_var, 
                                   values=["未开始", "进行中", "已完成"], width=37)
        status_combo.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 确认按钮
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="确认修改", command=self.confirm, width=20).pack(pady=10)
    
    def confirm(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("错误", "任务标题不能为空！")
            return
        
        updated_data = {
            "title": title,
            "description": self.desc_text.get("1.0", tk.END).strip(),
            "category": self.category_var.get(),
            "priority": self.priority_var.get(),
            "status": self.status_var.get(),
            "due_date": self.due_date_entry.get().strip()
        }
        
        self.task_service.update_task(self.task_id, updated_data)
        self.destroy()
