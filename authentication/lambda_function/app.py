import jwt
import datetime

# Replace this with your actual Supabase JWT secret
supabase_jwt_secret = '1ihaaCug9epxJMR8R/nb2an4sl80AMqow1S4Xz8uSrxgfpf1VQxP3gS92O626uiSsbKTefnbLgvCp8Jv+Aq+3Q=='

# Payload data for the JWT token
payload = {
    'sub': '629f8a9e-14e4-4bd3-9254-b79564caa241',
    'aud': 'authenticated',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expiration time
    'iss': 'https://egwyuljoijjiuoduculv.supabase.co',  # Issuer
    'email': 'bilalhassan590@gmail.com',
}

# Generate the JWT token
token = jwt.encode(payload, supabase_jwt_secret, algorithm='HS256')

print("Generated JWT Token:", token)
