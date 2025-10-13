import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 确保当前目录在模块搜索路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user_auth import UserAuth
from task_manager import TaskManagerFrame

class TaskManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("任务管理系统")
        self.root.geometry("800x600")
        
        self.user_auth = UserAuth()
        self.current_frame = None
        
        # 显示登录界面
        self.show_login_frame()

    def clear_frame(self):
        """清除当前界面"""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None

    def show_login_frame(self):
        """显示登录界面"""
        self.clear_frame()
        
        self.current_frame = ttk.Frame(self.root, padding="50")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(self.current_frame, text="任务管理系统", font=("Arial", 20)).grid(
            row=0, column=0, columnspan=2, pady=30
        )
        
        # 用户名
        ttk.Label(self.current_frame, text="用户名:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.username_var = tk.StringVar()
        ttk.Entry(self.current_frame, textvariable=self.username_var, width=30).grid(
            row=1, column=1, pady=10
        )
        
        # 密码
        ttk.Label(self.current_frame, text="密码:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.password_var = tk.StringVar()
        ttk.Entry(self.current_frame, textvariable=self.password_var, show="*", width=30).grid(
            row=2, column=1, pady=10
        )
        
        # 按钮区
        btn_frame = ttk.Frame(self.current_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="登录", command=self.handle_login, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="注册", command=self.show_register_frame, width=15).pack(side=tk.LEFT, padx=10)

    def show_register_frame(self):
        """显示注册界面"""
        self.clear_frame()
        
        self.current_frame = ttk.Frame(self.root, padding="50")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(self.current_frame, text="用户注册", font=("Arial", 20)).grid(
            row=0, column=0, columnspan=2, pady=30
        )
        
        # 用户名
        ttk.Label(self.current_frame, text="用户名:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.reg_username_var = tk.StringVar()
        ttk.Entry(self.current_frame, textvariable=self.reg_username_var, width=30).grid(
            row=1, column=1, pady=10
        )
        
        # 密码
        ttk.Label(self.current_frame, text="密码:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.reg_password_var = tk.StringVar()
        ttk.Entry(self.current_frame, textvariable=self.reg_password_var, show="*", width=30).grid(
            row=2, column=1, pady=10
        )
        
        # 确认密码
        ttk.Label(self.current_frame, text="确认密码:").grid(row=3, column=0, sticky=tk.W, pady=10)
        self.reg_confirm_var = tk.StringVar()
        ttk.Entry(self.current_frame, textvariable=self.reg_confirm_var, show="*", width=30).grid(
            row=3, column=1, pady=10
        )
        
        # 按钮区
        btn_frame = ttk.Frame(self.current_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="注册", command=self.handle_register, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="返回登录", command=self.show_login_frame, width=15).pack(side=tk.LEFT, padx=10)

    def show_task_manager(self):
        """显示任务管理界面"""
        self.clear_frame()
        
        # 顶部用户信息和登出按钮
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        username = self.user_auth.current_user["username"]
        ttk.Label(top_frame, text=f"当前用户: {username}").pack(side=tk.LEFT)
        ttk.Button(top_frame, text="退出登录", command=self.logout).pack(side=tk.RIGHT)
        
        # 任务管理主界面
        self.current_frame = TaskManagerFrame(
            self.root, 
            self.user_auth.current_user["id"]
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def handle_login(self):
        """处理登录逻辑"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空")
            return
            
        success, msg = self.user_auth.login(username, password)
        if success:
            self.show_task_manager()
        else:
            messagebox.showerror("登录失败", msg)

    def handle_register(self):
        """处理注册逻辑"""
        username = self.reg_username_var.get().strip()
        password = self.reg_password_var.get().strip()
        confirm = self.reg_confirm_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空")
            return
            
        success, msg = self.user_auth.register(username, password, confirm)
        if success:
            messagebox.showinfo("成功", msg)
            self.show_login_frame()
        else:
            messagebox.showerror("注册失败", msg)

    def logout(self):
        """处理登出"""
        self.user_auth.logout()
        self.show_login_frame()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagementSystem(root)
    root.mainloop()
    