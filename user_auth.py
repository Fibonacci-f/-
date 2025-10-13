import hashlib
import uuid
from datetime import datetime
from data_storage import DataStorage

class UserAuth:
    def __init__(self):
        self.storage = DataStorage()
        self.current_user = None

    @staticmethod
    def hash_password(password):
        """密码加密"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password, confirm_password):
        """用户注册"""
        if password != confirm_password:
            return False, "两次密码输入不一致"
            
        if len(password) < 6:
            return False, "密码长度不能少于6位"
            
        users = self.storage.load_users()
        if any(user["username"] == username for user in users):
            return False, "用户名已存在"
            
        # 创建新用户
        new_user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "password": self.hash_password(password),
            "register_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users.append(new_user)
        self.storage.save_users(users)
        return True, "注册成功"

    def login(self, username, password):
        """用户登录"""
        users = self.storage.load_users()
        hashed_pwd = self.hash_password(password)
        
        for user in users:
            if user["username"] == username and user["password"] == hashed_pwd:
                self.current_user = user
                return True, "登录成功"
                
        return False, "用户名或密码错误"

    def logout(self):
        """用户登出"""
        self.current_user = None
if __name__ == "__main__":
    pass