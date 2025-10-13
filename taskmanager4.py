import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta  # 添加timedelta导入

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("小型任务管理系统")
        self.root.geometry("800x600")
        
        self.data_file = "tasks.json"
        self.tasks = self.load_tasks()
        
        self.create_widgets()
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_tasks(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        # 顶部功能按钮区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="添加任务", command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="编辑任务", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="删除任务", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="刷新列表", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        
        # 任务列表显示区
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("id", "title", "category", "priority", "status", "due_date", "create_time")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="任务标题")
        self.tree.heading("category", text="分类")
        self.tree.heading("priority", text="优先级")
        self.tree.heading("status", text="状态")
        self.tree.heading("due_date", text="截止日期")
        self.tree.heading("create_time", text="创建时间")
        
        self.tree.column("id", width=50)
        self.tree.column("title", width=150)
        self.tree.column("category", width=100)
        self.tree.column("priority", width=100)
        self.tree.column("status", width=100)
        self.tree.column("due_date", width=120)
        self.tree.column("create_time", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.refresh_list()
    
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.tasks:
            self.tree.insert("", tk.END, values=(
                task["id"], task["title"], task["category"], task["priority"], 
                task["status"], task["due_date"], task["create_time"]
            ))
    
    def add_task(self):
        # 调整弹窗大小和布局，确保所有组件可见
        dialog = tk.Toplevel(self.root)
        dialog.title("添加任务")
        dialog.geometry("600x500")  # 增加宽度和高度
        dialog.resizable(True, True)  # 允许窗口 resize
        
        # 创建一个容器框架，方便管理布局
        container = ttk.Frame(dialog, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # 任务标题
        ttk.Label(container, text="任务标题:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        title_entry = ttk.Entry(container, width=40)
        title_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 任务描述
        ttk.Label(container, text="任务描述:").grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)
        desc_text = tk.Text(container, width=30, height=5)
        desc_text.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        # 任务分类
        ttk.Label(container, text="任务分类:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(container, textvariable=category_var, 
                                      values=["工作", "学习", "生活", "其他"], width=37)
        category_combo.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        category_combo.current(0)
        
        # 优先级
        ttk.Label(container, text="优先级:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(container, textvariable=priority_var, 
                                      values=["高", "中", "低"], width=37)
        priority_combo.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        priority_combo.current(1)
        
        # 截止日期
        ttk.Label(container, text="截止日期:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        due_date_entry = ttk.Entry(container, width=40)
        due_date_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        tomorrow = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + 
                   timedelta(days=1)).strftime("%Y-%m-%d")  # 修正：使用timedelta而不是datetime.timedelta
        due_date_entry.insert(0, tomorrow)
        
        # 任务状态
        ttk.Label(container, text="状态:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(container, textvariable=status_var, 
                                   values=["未开始", "进行中", "已完成"], width=37)
        status_combo.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)
        status_combo.current(0)
        
        # 确认添加按钮 - 确保在可见区域
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        def confirm():
            title = title_entry.get().strip()
            if not title:
                messagebox.showerror("错误", "任务标题不能为空！")
                return
            
            desc = desc_text.get("1.0", tk.END).strip()
            category = category_var.get()
            priority = priority_var.get()
            due_date = due_date_entry.get().strip()
            status = status_var.get()
            create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            task_id = str(int(datetime.now().timestamp()))
            
            new_task = {
                "id": task_id,
                "title": title,
                "description": desc,
                "category": category,
                "priority": priority,
                "status": status,
                "due_date": due_date,
                "create_time": create_time
            }
            
            self.tasks.append(new_task)
            self.save_tasks()
            self.refresh_list()
            dialog.destroy()
        
        # 确认按钮设置更大的尺寸和明确的位置
        ttk.Button(btn_frame, text="确认添加", command=confirm, width=20).pack(pady=10)
    
    def edit_task(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选中一个任务！")
            return
        
        item = selected_items[0]
        values = self.tree.item(item, "values")
        task_id = values[0]
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        
        if not task:
            messagebox.showerror("错误", "未找到该任务的数据！")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑任务")
        dialog.geometry("600x500")
        dialog.resizable(True, True)
        
        container = ttk.Frame(dialog, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(container, text="任务标题:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        title_entry = ttk.Entry(container, width=40)
        title_entry.insert(0, task["title"])
        title_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(container, text="任务描述:").grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)
        desc_text = tk.Text(container, width=30, height=5)
        desc_text.insert("1.0", task["description"])
        desc_text.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(container, text="任务分类:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(container, textvariable=category_var, 
                                      values=["工作", "学习", "生活", "其他"], width=37)
        category_combo.insert(0, task["category"])
        category_combo.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(container, text="优先级:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(container, textvariable=priority_var, 
                                      values=["高", "中", "低"], width=37)
        priority_combo.insert(0, task["priority"])
        priority_combo.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(container, text="截止日期:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        due_date_entry = ttk.Entry(container, width=40)
        due_date_entry.insert(0, task["due_date"])
        due_date_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(container, text="状态:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(container, textvariable=status_var, 
                                   values=["未开始", "进行中", "已完成"], width=37)
        status_combo.insert(0, task["status"])
        status_combo.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)
        
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        def confirm():
            title = title_entry.get().strip()
            if not title:
                messagebox.showerror("错误", "任务标题不能为空！")
                return
            
            desc = desc_text.get("1.0", tk.END).strip()
            category = category_var.get()
            priority = priority_var.get()
            due_date = due_date_entry.get().strip()
            status = status_var.get()
            
            task["title"] = title
            task["description"] = desc
            task["category"] = category
            task["priority"] = priority
            task["due_date"] = due_date
            task["status"] = status
            
            self.save_tasks()
            self.refresh_list()
            dialog.destroy()
        
        ttk.Button(btn_frame, text="确认修改", command=confirm, width=20).pack(pady=10)
    
    def delete_task(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选中一个任务！")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的任务吗？"):
            item = selected_items[0]
            values = self.tree.item(item, "values")
            task_id = values[0]
            
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
            self.save_tasks()
            self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()