import bcrypt


HASH_WORK_FACTOR = 15 


def hash_password(plain_text_password): 
    salt = bcrypt.gensalt(rounds=HASH_WORK_FACTOR) 
    encoded_password = plain_text_password.encode() 
 
    return bcrypt.hashpw(encoded_password, salt)
