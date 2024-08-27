from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.response import respond_error, respond_success
from mails.send_mail import send_mail
from database.models import User, Plan, AuthSession
from database.setup import SessionLocal
from sqlalchemy import update
import bcrypt



authrouter = APIRouter(prefix="/auth",tags=["auth"])

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

    with SessionLocal() as session:
        user = session.query(User).filter_by(email=body.email).first()
        if not user:
            return JSONResponse(respond_error("Invalid Login Credentials"), status_code = 401)
        
        if bcrypt.checkpw(body.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            if user.is_active:
                # generate jwt token
                return JSONResponse(respond_success({
                    "token": "random token",
                }, "Logged in successfully"))
            else:
                send_mail(user.name, user.email, "Activate account to login", "Click this link to activate your account", "Click this link to activate your account")
                return JSONResponse(respond_success(None, "Please activate your account. A mail has been sent to your email address"))
        else:
            return JSONResponse(respond_error("Invalid Login Credentials"), status_code = 401)            

    

@authrouter.post("/register", tags=["auth"], response_class=JSONResponse)
def register(body: RegisterBody):
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
                plan = session.query(Plan).filter_by(title = "Free Plan").first()
                if not plan:
                    print("Free plan does not exist in database")
                    return JSONResponse(respond_error("Internal Server error"), status_code=500)
                
                password_hash = bcrypt.hashpw(body.password.encode('utf-8'), bcrypt.gensalt())
                user = User(name = body.name, email = body.email, hashed_password = password_hash.decode(), plan=plan.id)
                authsession = AuthSession(type = "email_validation", user = user)

                session.add(user)
                session.add(authsession)
                session.commit()

                print(authsession.key)

             res: str = send_mail(body.name, body.email, "Welcome to CraftMyCV.", f"this is to welcome you to craft my cv <button><a href = \"http://localhost:8000/auth/verify-email/{authsession.key}\">click to verify email</a></button>", f'this is to welcome you to craft my cv. Link: http://localhost:8000/auth/verify-email/{authsession.key}')
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