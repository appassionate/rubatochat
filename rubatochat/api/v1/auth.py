from typing import Union, Optional
from datetime import datetime, timedelta

from pydantic import BaseModel
from jose import JWTError, jwt

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from rubatochat.core.database.models import User, add_item, User
from rubatochat.api import db_engine, ALGORITHM, SECRET_KEY
from rubatochat.utils.logger import logger
from rubatochat.core.database.models import User, OpenAIKEYS, Session, add_item, delete_item_by_id, select

# followed https://www.youtube.com/watch?v=5GxQ1rLTwaU


# ALGORITHM = "HS256"
# SECRET_KEY = "7de1d69f6b24b5c4137385c4cb18fa5598d29f852dab936bcd60adb00652577c"

# 使用sha256算法进行密码加密
from passlib.context import CryptContext


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
    scopes: list = []

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    # 验证明文密码与哈希密码是否匹配
    return pwd_context.verify(plain_password, hashed_password)

def encrypt_password(plain_password):
    # 使用 pbkdf2_sha256 哈希算法进行密码加密
    return pwd_context.hash(plain_password)


# def encrypt_password(plain_password):
#     # 使用 pbkdf2_sha256 哈希算法进行密码加密
#     hashed_password = pbkdf2_sha256.hash(plain_password)
#     return hashed_password

# 注册的api
app = APIRouter()

@app.post("/register")
async def register(username:str, #注册的校验，pydantic?
                   password:str, 
                   email:Union[str, None] = None, 
                   fullname:Union[str, None] = None, 
                   ):
    
    hashed_pw = encrypt_password(password)
    add_item(db_engine, 
             item_type="user", 
             username=username, 
             password=hashed_pw,
             email=email, 
             fullname=fullname, 
             disabled=False,
             created_at=datetime.utcnow())
    
    
    logger.info("user: "+username+" register success")

    #TODO: 自动登录，返回token，重定向
    return {"message": {"username":username}}


def get_user(username):

    with Session(db_engine) as session:
        stmt = select(User).where(User.username == username)
        user = session.exec(stmt)
        user = user.first()
    if not user:
        return None
    return user

#登录的api实现
def authenticate_user(username:str, password:str):

    user = get_user(username)
    if not user:
        return False
    _saved_pw = user.password
    _is_valid = verify_password(password, _saved_pw)
    if not _is_valid:
        return False
    
    return user

# 使用jwt进行token的生成，算法为HS256，密钥为SECRET_KEY
def create_access_token(data:dict, expires_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 验证token是否有效
    #该方法仅依赖oauth2_scheme
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        #解码token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        #根据解密后的token获取用户名信息
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    user.password = "notneedhere"

    return user

async def get_current_active_user(current_user:User = Depends(get_current_user)):
    
    #验证用户是否被禁用
    #掩盖密码
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    current_user.password = "notneedhere"
    return current_user


@app.post("/token", response_model=Token) #定义返回的数据模型, 序列化
async def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends()):
    #登录，返回token
    #该方法依赖OAuth2PasswordRequestForm
    #form_data是oauth进行登录后得到的数据
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, 
                            detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub":user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, 
            "token_type": "bearer",}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    #获取用户信息
    #掩盖密码
    return User(**current_user.dict())

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    #获取用户的items
    return [{"item_id": "Foo", "owner": current_user}]

