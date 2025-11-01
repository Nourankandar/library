from database.verification import verification
from database.users import Users
import datetime
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def verify_user_code(email, code, purpose):

    db = Users()
    verify=verification()
    user = db.get_user_login(email.get())
    print(user)
    if user is None:
        print("1")
        return None
    user_id = user[0]
    code_data = verify.get_verification_code_data(user_id, code, purpose)
    if code_data is None:
        print("2")
        return False

    retrieved_code, expires_at = code_data
    if expires_at < datetime.datetime.now():
        verify.activate_user_and_delete_code(user_id, purpose)
        print("3")
        return False
    if code == retrieved_code:
        success = verify.activate_user_and_delete_code(user_id, purpose)
        if success:
            print("4")
            return True
        else:
            print("5")
            return False
    return False