import json
import os
import datetime
SESSION_FILE = 'session.json'

def save_session(user_id, user_role):
    """تحفظ حالة المستخدم محلياً."""
    session_data = {
        'user_id': user_id,
        'user_role': user_role,
        'timestamp': str(datetime.datetime.now()) 
    }
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_data, f)
    except Exception as e:
        print(f"Error saving session: {e}")

def load_session():
    """تحمّل حالة المستخدم المحفوظة محلياً، أو تُرجع None."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                data = json.load(f)
                return data.get('user_id'), data.get('user_role')
        except Exception as e:
            print(f"Error loading session file: {e}")
            return None, None
    return None, None

def delete_session():
    """تحذف ملف الجلسة عند تسجيل الخروج."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print("Session file deleted.")