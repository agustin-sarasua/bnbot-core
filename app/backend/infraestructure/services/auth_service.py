from jose import JWTError, jwt
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Depends, Security, HTTPException
from app.backend.domain.entities import TokenData
from app.utils import logger
import json
from six.moves.urllib.request import urlopen
from functools import wraps

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace these with your Auth0 config
AUTH0_DOMAIN = 'dev-szxtl072nd0t8rsr.us.auth0.com'
API_AUDIENCE = 'https://dev-szxtl072nd0t8rsr.us.auth0.com/api/v2/'
ALGORITHMS = ["RS256"]

def validate_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    logger.debug(f"Tokennn: {token}")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
        
            sub: str = payload.get("sub")
            if sub is None:
                raise credentials_exception
            token_data = TokenData(sub=sub)
            return token_data
        
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception
    