## ...

***
## Tools:

***
## API
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
>                                           messages | String
>                                           status   | String (review, blocked, correct)
>                                           success  | String
>                                           user_id  | Integer                    
>      
>      {'messages': 'АБРАКАДАБРА'}
          
***
   
