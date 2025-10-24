from database.verification import verification
from database.users import Users
import datetime
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def verify_user_code(self, email, code, purpose):
    db = Users()
    verify=verification()
    user = db.get_user_login(email)
    if user is None:
        return None
    user_id = user[0]
    code_data = verify.get_verification_code_data(user_id, code, purpose)
    if code_data is None:
        return False
    retrieved_code, expires_at = code_data
    if expires_at < datetime.datetime.now():
        verify.activate_user_and_delete_code(user_id, purpose)
        return False,
    if code == retrieved_code:
        success = verify.activate_user_and_delete_code(user_id, purpose)
        if success:
            return True,
        else:
            return False
    return False