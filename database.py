import jwt
token =  jwt.encode(
    {"c_id":2},
    "secret",
    algorithm='HS256'
)            
print(token)
data = jwt.decode(token, "secret", algorithms="HS256")
print(data)