import bcrypt
password = "data"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

hashed_str = hashed_password.decode('utf-8')


print(hashed_str)