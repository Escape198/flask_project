## REST API Flask, SQLAlchemy. 🍪

Authentication: **JWTManager**

Testing: **PyTest**

Serialization/Deserialization: **Marshmallow**
5
Exception handling and logging
***
## Task description 🍪
Client sends a message to API service.
The service saves the message in the database (think of the table(s) yourself) with the status "in review". In the database the message can be in three states: checked, blocked, correct.

API service changes the status of the message. If the message is correct, it is set to "correct", otherwise it is set to "blocked".
***
Create a virtual environment
>python -m venv env


Activate the venv
>env\scripts\activate.bat


Open the project folder
>cd project


Install all modules
>pip install -r requirements.txt


Starting the server
>python manage.py
***
## API 🍪
-     /auth || POST
      Exchanging user login and password to JWT authorization token.
>      
>      Parameters:                         Response:
>      email    | String                   success      | String      
>      password | String                   access_token | String
>      
>      {"email": "test@gmail.com","password": "Никита,сДР!"}
----

-      /sign-up || POST
      New user registration.
>      
>       Parameters:                         Response:
>       name     | String(50)               success | String    
>       email    | String(50)                   
>       password | String(50)      
>      
>      {'name': 'juice', 'email': 'test@test.com', 'password': 'test'}
----

-      /api/v1/message || POST
      Send a message to the database
>      
>       Parameters:                         Response:
>       message  | String(500)              id | Integer
>       'Authorization': 'Bearer {}         messages | String
>                                           status   | String (review, blocked, correct)
>                                           success  | String (Check text status)
>                                           user_id  | Integer                    
>      
>      {'messages': 'АБРАКАДАБРА'}
----

-      /api/v1/message || GET
      Get a list of all your messages
>      
>       Parameters:                         Response:
>       'Authorization': 'Bearer {}         id | Integer
>                                           messages | String
>                                           status   | String (review, blocked, correct)
>                                           success  | String (Check text status)
>                                           user_id  | Integer                    
>      
>        
***
   
