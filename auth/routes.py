from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.response import respond_error, respond_success
from mails.send_mail import send_mail
from database.models import Subscription, User, Plan, AuthSession
from database.setup import SessionLocal
from sqlalchemy import update
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

authrouter = APIRouter(prefix="/auth",tags=["auth"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    with SessionLocal() as session:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            raise credentials_exception
        return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(token)

class LoginBody(BaseModel):
     email: str
     password: str


class RegisterBody(BaseModel):
    email: str
    password: str
    conf_password: str
    name: str
    accept_t_and_c: bool


@authrouter.post("/login", tags=["auth"], response_class=JSONResponse)
def login(body: LoginBody):
    print(body)

    with SessionLocal() as session:
        user = session.query(User).filter_by(email=body.email).first()
        if not user:
            return JSONResponse(respond_error("Invalid Login Credentials"), status_code = 401)
        
        if bcrypt.checkpw(body.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            if user.is_active:
                access_token = create_access_token(data={"email": user.email})
                active_subscription = session.query(Subscription).filter(Subscription.user_id == user.id, Subscription.end_date > datetime.now()).first()
                plan = active_subscription.plan if active_subscription else None

                return JSONResponse(respond_success({
                    "token": access_token,
                    "user_id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                    "plan": plan.title if plan else "No Plan (FREE)",
                    "is_active": user.is_active,
                    "has_valid_subscription": active_subscription is not None,
                }, "Logged in successfully"))
            
            else:
                send_mail(user.name, user.email, "Activate account to login", "Click this link to activate your account", "Click this link to activate your account")
                return JSONResponse(respond_success(None, "Please activate your account. A mail has been sent to your email address"))
        else:
            return JSONResponse(respond_error("Invalid Login Credentials"), status_code = 401)            

    

@authrouter.post("/register", tags=["auth"], response_class=JSONResponse)
async def register(body: RegisterBody, request: Request):
    base_url = str(request.base_url)
    if not body.accept_t_and_c:
        return respond_error("User needs to accept terms and conditions")
    else:
        errors = []
        if not is_valid_email(body.email):
             errors.append("Invalid email address")
        if not (body.password == body.conf_password):
             errors.append("Password do not match")
        if len(body.name.split(" ")) < 2:
             errors.append("First name and last name required")
        
        if len(errors) > 0:
             return JSONResponse(respond_error(error=errors), status_code=400)
        else:
             with SessionLocal() as session:                
                password_hash = bcrypt.hashpw(body.password.encode('utf-8'), bcrypt.gensalt())
                user = User(name = body.name, email = body.email, hashed_password = password_hash.decode())
                authsession = AuthSession(type = "email_validation", user = user)

                session.add(user)
                session.add(authsession)
                session.commit()

                verification_link = f"{base_url}auth/verify-email/{authsession.key}"

                html_content = f"Welcome to CraftMyCV. <a href='{verification_link}'>Click here to verify your email</a>"
                plain_text = f"Welcome to CraftMyCV. Verify your email at: {verification_link}"

                res: str = send_mail(body.name, body.email, "Welcome to CraftMyCV.", html_content, plain_text)
             if res.find("20") != -1:
                  return JSONResponse(respond_success(200, "Registration completed. Please verify your email"))
             else:
                  return JSONResponse(respond_error("Failed to complete registration. Please try again"), status_code=500)


@authrouter.get("/verify-email/{token}", tags=["auth"], response_class=JSONResponse)
def verify_email(token: str):
       with SessionLocal() as session:
           auth_session = session.query(AuthSession).filter_by(key = token).first()
           if not auth_session:
               return JSONResponse(respond_error("Invalid verification token"), status_code=400)
           
           try:
                session.execute(
                    update(User)
                    .where(User.id == auth_session.user_id)
                    .values(is_active = True)
                    )
                session.delete(auth_session)
                session.commit()     
                return JSONResponse(respond_success(None, "Email verified successfully"))
           except Exception as e:
                return JSONResponse(respond_error("error validating token"))
   
import re
def is_valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))