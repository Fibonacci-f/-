import tkinter as tk
from tkinter import ttk, messagebox
from core.task_service import TaskService
from ui.dialogs import AddTaskDialog, EditTaskDialog

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("小型任务管理系统")
        self.root.geometry("1000x700")
        
        # 初始化服务
        self.task_service = TaskService()
        
        # 创建界面
        self.create_widgets()
        self.refresh_task_list()
    
    def create_widgets(self):
        # 主容器
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部功能按钮区
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(btn_frame, text="添加任务", command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="编辑任务", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="删除任务", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="刷新列表", command=self.refresh_task_list).pack(side=tk.LEFT, padx=5)
        
        # 搜索过滤区
        search_frame = tk.LabelFrame(main_frame, text="搜索过滤", padx=10, pady=10)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 关键词搜索
        tk.Label(search_frame, text="关键词:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # 分类过滤
        tk.Label(search_frame, text="分类:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar(value="全部")
        category_combo = ttk.Combobox(search_frame, textvariable=self.category_var, 
                                     values=["全部", "工作", "学习", "生活", "其他"], width=10)
        category_combo.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        category_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # 优先级过滤
        tk.Label(search_frame, text="优先级:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.priority_var = tk.StringVar(value="全部")
        priority_combo = ttk.Combobox(search_frame, textvariable=self.priority_var, 
                                     values=["全部", "高", "中", "低"], width=10)
        priority_combo.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        priority_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # 状态过滤
        tk.Label(search_frame, text="状态:").grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
        self.status_var = tk.StringVar(value="全部")
        status_combo = ttk.Combobox(search_frame, textvariable=self.status_var, 
                                   values=["全部", "未开始", "进行中", "已完成"], width=10)
        status_combo.grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
        status_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # 清除过滤按钮
        tk.Button(search_frame, text="清除过滤", command=self.clear_filters).grid(row=0, column=8, padx=10, pady=5)
        
        # 内容区域（统计面板和任务列表）
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧统计面板
        self.create_stats_panel(content_frame)
        
        # 右侧任务列表
        list_frame = tk.LabelFrame(content_frame, text="任务列表", padx=10, pady=10)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
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
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def create_stats_panel(self, parent):
        """创建统计面板"""
        stats_frame = tk.LabelFrame(parent, text="任务统计", padx=10, pady=10, width=200)
        stats_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        stats_frame.pack_propagate(False)  # 固定宽度
        
        # 总任务数
        self.total_label = tk.Label(stats_frame, text="总任务数: 0", font=("Arial", 12, "bold"))
        self.total_label.pack(anchor=tk.W, pady=5)
        
        # 按分类统计
        tk.Label(stats_frame, text="按分类:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.category_stats = tk.Label(stats_frame, text="", justify=tk.LEFT)
        self.category_stats.pack(anchor=tk.W, pady=5)
        
        # 按优先级统计
        tk.Label(stats_frame, text="按优先级:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.priority_stats = tk.Label(stats_frame, text="", justify=tk.LEFT)
        self.priority_stats.pack(anchor=tk.W, pady=5)
        
        # 按状态统计
        tk.Label(stats_frame, text="按状态:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.status_stats = tk.Label(stats_frame, text="", justify=tk.LEFT)
        self.status_stats.pack(anchor=tk.W, pady=5)
        
        # 刷新统计按钮
        tk.Button(stats_frame, text="刷新统计", command=self.refresh_stats).pack(pady=10)
    
    def refresh_task_list(self, tasks=None):
        """刷新任务列表"""
        # 清空现有列表
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 加载并显示所有任务或过滤后的任务
        if tasks is None:
            tasks = self.task_service.get_all_tasks()
        
        for task in tasks:
            self.tree.insert("", tk.END, values=(
                task["id"], task["title"], task["category"], task["priority"], 
                task["status"], task["due_date"], task["create_time"]
            ))
        
        # 刷新统计信息
        self.refresh_stats()
    
    def refresh_stats(self):
        """刷新统计信息"""
        tasks = self.task_service.get_all_tasks()
        stats = self.task_service.get_task_statistics()
        
        # 更新总任务数
        self.total_label.config(text=f"总任务数: {stats['total_tasks']}")
        
        # 更新分类统计
        category_text = ""
        for category, count in stats['by_category'].items():
            category_text += f"{category}: {count}\n"
        self.category_stats.config(text=category_text)
        
        # 更新优先级统计
        priority_text = ""
        for priority, count in stats['by_priority'].items():
            priority_text += f"{priority}: {count}\n"
        self.priority_stats.config(text=priority_text)
        
        # 更新状态统计
        status_text = ""
        for status, count in stats['by_status'].items():
            status_text += f"{status}: {count}\n"
        self.status_stats.config(text=status_text)
    
    def on_search_change(self, event=None):
        """搜索条件变化时的处理"""
        self.apply_filters()
    
    def on_filter_change(self, event=None):
        """过滤条件变化时的处理"""
        self.apply_filters()
    
    def apply_filters(self):
        """应用所有过滤条件"""
        keyword = self.search_var.get().strip().lower()
        category = self.category_var.get()
        priority = self.priority_var.get()
        status = self.status_var.get()
        
        filtered_tasks = self.task_service.filter_tasks(
            keyword=keyword if keyword else None,
            category=category if category != "全部" else None,
            priority=priority if priority != "全部" else None,
            status=status if status != "全部" else None
        )
        
        self.refresh_task_list(filtered_tasks)
    
    def clear_filters(self):
        """清除所有过滤条件"""
        self.search_var.set("")
        self.category_var.set("全部")
        self.priority_var.set("全部")
        self.status_var.set("全部")
        self.refresh_task_list()
    
    def add_task(self):
        """打开添加任务对话框"""
        dialog = AddTaskDialog(self.root, self.task_service)
        self.root.wait_window(dialog)
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