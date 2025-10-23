import tkinter as tk
from tkinter import ttk, messagebox
from core.task_service import TaskService
from ui.dialogs import AddTaskDialog, EditTaskDialog

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("小型任务管理系统")
        self.root.geometry("800x600")
        
        # 初始化服务
        self.task_service = TaskService()
        
        # 创建界面
        self.create_widgets()
        self.refresh_task_list()
    
    def create_widgets(self):
        # 顶部功能按钮区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="添加任务", command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="编辑任务", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="删除任务", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="刷新列表", command=self.refresh_task_list).pack(side=tk.LEFT, padx=5)
        
        # 任务列表显示区
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("id", "title", "category", "priority", "status", "due_date", "create_time")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="任务标题")
        self.tree.heading("category", text="分类")
        self.tree.heading("priority", text="优先级")
        self.tree.heading("status", text="状态")
        self.tree.heading("due_date", text="截止日期")
        self.tree.heading("create_time", text="创建时间")
        
        # 设置列宽
        self.tree.column("id", width=50)
        self.tree.column("title", width=150)
        self.tree.column("category", width=100)
        self.tree.column("priority", width=100)
        self.tree.column("status", width=100)
        self.tree.column("due_date", width=120)
        self.tree.column("create_time", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def refresh_task_list(self):
        """刷新任务列表"""
        # 清空现有列表
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 加载并显示所有任务
        tasks = self.task_service.get_all_tasks()
        for task in tasks:
            self.tree.insert("", tk.END, values=(
                task["id"], task["title"], task["category"], task["priority"], 
                task["status"], task["due_date"], task["create_time"]
            ))
    
    def add_task(self):
        """打开添加任务对话框"""
        dialog = AddTaskDialog(self.root, self.task_service)
        self.root.wait_window(dialog)  # 等待对话框关闭
        if dialog.result:
            self.refresh_task_list()
    
    def edit_task(self):
        """打开编辑任务对话框"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选中一个任务！")
            return
        
        item = selected_items[0]
        task_id = self.tree.item(item, "values")[0]
        
        dialog = EditTaskDialog(self.root, self.task_service, task_id)
        self.root.wait_window(dialog)
        self.refresh_task_list()
    
    def delete_task(self):
        """删除选中的任务"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选中一个任务！")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的任务吗？"):
            item = selected_items[0]
            task_id = self.tree.item(item, "values")[0]
            if self.task_service.delete_task(task_id):
                self.refresh_task_list()
