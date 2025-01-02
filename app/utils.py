from passlib.context import CryptContext

# telling what the default hashing algorithm is- in this case bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)