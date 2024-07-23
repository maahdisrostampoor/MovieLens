import jwt
import json

# Replace this with your actual Supabase JWT secret
supabase_jwt_secret = '1ihaaCug9epxJMR8R/nb2an4sl80AMqow1S4Xz8uSrxgfpf1VQxP3gS92O626uiSsbKTefnbLgvCp8Jv+Aq+3Q=='

# The JWT token you want to verify
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MjlmOGE5ZS0xNGU0LTRiZDMtOTI1NC1iNzk1NjRjYWEyNDEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzIwOTA1NjUyLCJpc3MiOiJodHRwczovL2Vnd3l1bGpvaWpqaXVvZHVjdWx2LnN1cGFiYXNlLmNvIiwiZW1haWwiOiJiaWxhbGhhc3NhbjU5MEBnbWFpbC5jb20ifQ.VCSpnBeqQxEdBcuIrjYyx1UIhltiuDzoPxOBzYutXmw'

try:
    # Decode the JWT token
    decoded_token = jwt.decode(token, supabase_jwt_secret, algorithms=['HS256'], audience='authenticated')
    print("Decoded Token:", json.dumps(decoded_token, indent=4))  # Pretty-print the decoded token
except jwt.ExpiredSignatureError:
    print("Token has expired.")
except jwt.InvalidTokenError as e:
    print("Invalid token:", str(e))
