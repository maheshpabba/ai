from starlette.responses import RedirectResponse
from controllers.Db import MongoController
from conf.models import Session
from json.decoder import JSONDecodeError
from urllib.parse import quote
from fastapi import Request
from bson import ObjectId
from base64 import b64encode
from functools import wraps
from typing import Dict
import json
import logging
import traceback
import datetime
import jwt
import requests


logger = logging.getLogger(__name__)


class OpenIDConnect:
    well_known_pattern = "{}/.well-known/openid-configuration"

    def __init__(
        self, scope:str,client_id:str,client_secret:str,sso_host:str
    ) -> None:
        # self.scope = "openid profile email"
        # self.client_id = "DI4V9IHNR9S4Y7I63PDL"
        # self.client_secret = "i3WbWrhBk0s9mJCP8AiuyAdRFbNUTz3UJAJ9oB1Q"
        # self.host="https://sso-dbbfec7f.sso.duosecurity.com/oidc/DI4V9IHNR9S4Y7I63PDL"

        # self.client_id = "dcaf-ai"
        # self.client_secret = "i3WbWrhBk0s9mJCP8AiuyAdRFbNUTz3UJAJ9oB1Q"
        # self.host="https://cloudsso.cisco.com"
        self.scope=scope
        self.client_id=client_id
        self.client_secret=client_secret
        self.host=sso_host
        self.db = MongoController()
        endpoints = self.to_dict_or_raise(
            requests.get(self.well_known_pattern.format(self.host))
        )
        self.issuer = endpoints.get("issuer")
        self.authorization_endpoint = endpoints.get("authorization_endpoint")
        self.token_endpoint = endpoints.get("token_endpoint")
        self.introspect_token = endpoints.get("introspection_endpoint")
        self.userinfo_endpoint = endpoints.get("userinfo_endpoint")
        self.jwks_uri = endpoints.get("jwks_uri")

    def authenticate(
        self, code: str, callback_uri: str, get_user_info: bool = False
    ) -> Dict:
        logger.debug('Validating Token')
        auth_token = self.get_auth_token(code, callback_uri)
        id_token = auth_token.get("id_token")
        try:
            alg = jwt.get_unverified_header(id_token).get("alg")
        except Exception as e:
            logging.warning("Error getting unverified header in jwt.")
            raise Exception
        validated_token = self.obtain_validated_token(alg, id_token)
        if not get_user_info:
            return validated_token
        user_info = self.get_user_info(auth_token.get("access_token"))
        user_det={}
        session={}
        user_det["id"]=user_info.get('sub')
        user_det['title']=user_info.get('title')
        user_det['givenName']=user_info.get('given_name')
        user_det['familyName']=user_info.get('family_name')
        user_det['fullName']=user_info.get('fullname')
        user_det['email']=user_info.get('email')
        user_det['role'] = 'Manager' if "CN=all-senior-mgmt,OU=Cisco Groups,O=cco.cisco.com" in user_info.get('memberof') else 'User'
        self.validate_sub_matching(validated_token, user_info)
        session['accessToken']=auth_token.get('access_token')
        session['refreshToken']=auth_token.get('refresh_token')
        session['expiry']=auth_token.get('expires_in')
        session['redirectPath']=""
        session['ts']=datetime.datetime.now()
        session['lastRefresh']=""
        session['user']=user_det
        try:
            s=Session(**session)
            logging.debug(s.dict())
            id=self.db._create_user_session(s.dict())
            session['id']=str(id)
        except Exception as e:
            logger.error('Exception Received: %s',e)
        return session

    def get_auth_redirect_uri(self, callback_uri):
        return "{}?client_id={}&redirect_uri={}&response_type=code&scope={}".format(  # noqa
            self.authorization_endpoint,
            self.client_id,
            quote(callback_uri),
            self.scope,
        )

    def get_auth_token(self, code: str, callback_uri: str) -> str:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "redirect_uri": callback_uri,
        }
        logger.info(data)
        response = requests.post(
            self.token_endpoint, data=data
        )
        logger.info(response.json())
        return self.to_dict_or_raise(response)


    def validate_token(self,code:str) -> str:
        data={
            "token": code,
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            
        }
        response=requests.post(
            self.introspect_token,data=data
        )
        logger.info(data)
        return self.to_dict_or_raise(response)

    def obtain_validated_token(self, alg: str, id_token: str) -> Dict:
        if alg == "HS256":
            try:
                return jwt.decode(
                    id_token,
                    self.client_secret,
                    algorithms=["HS256"],
                    audience=self.client_id,
                )
            except Exception as e:
                logger.error("An error occurred while decoding the id_token")
                raise Exception(
                    "An error occurred while decoding the id_token"
                )
        elif alg == "RS256":
            response = requests.get(self.jwks_uri)
            web_key_sets = self.to_dict_or_raise(response)
            jwks = web_key_sets.get("keys")
            public_key = self.extract_token_key(jwks, id_token)
            try:
                return jwt.decode(
                    id_token,
                    key=public_key,
                    algorithms=["RS256"],
                    audience=self.client_id,
                    options={"verify_iat":False}
                )
            except Exception as e:
                logger.error("An error occurred while decoding the id_token")
                raise Exception(
                    "An error occurred while decoding the id_token"
                )
        else:
            raise Exception("Unsupported jwt algorithm found.")

    def extract_token_key(self, jwks: Dict, id_token: str) -> str:
        public_keys = {}
        for jwk in jwks:
            kid = jwk.get("kid")
            if not kid:
                continue
            try:
                k= jwt.algorithms.RSAAlgorithm.from_jwk(
                    json.dumps(jwk)
                )
            except:
                continue
            else:
                public_keys[kid]=k
        logger.debug("extracted public keys")
        try:
            kid = jwt.get_unverified_header(id_token).get("kid")
        except Exception as e:
            logger.warning("kid could not be extracted.")
            raise Exception("kid could not be extracted.")
        return public_keys.get(kid)

    def get_user_info(self, access_token: str) -> Dict:
        bearer = "Bearer {}".format(access_token)
        headers = {"Authorization": bearer}
        response = requests.get(self.userinfo_endpoint, headers=headers)
        return self.to_dict_or_raise(response)

    @staticmethod
    def validate_sub_matching(token: Dict, user_info: Dict) -> None:
        token_sub = ""  # nosec
        if token:
            token_sub = token.get("sub")
        if token_sub != user_info.get("sub") or not token_sub:
            logger.warning("Subject mismatch error.")
            raise Exception("Subject mismatch error.")

    @staticmethod
    def to_dict_or_raise(response: requests.Response) -> Dict:
        if response.status_code != 200:
            logger.error(f"Returned with status {response.status_code}.")
            raise Exception(
                f"Status code {response.status_code} for {response.url}."
            )
        try:
            return response.json()
        except JSONDecodeError:
            logger.error("Unable to decode json.")
            raise Exception(
                "Was not able to retrieve data from the response."
            )

    def require_login(self, view_func):
        @wraps(view_func)
        async def decorated(
            request: Request, get_user_info: bool = True, *args, **kwargs
        ):
            path1='/api/login'
            callback_uri = f"{request.url.scheme}://{request.url.netloc}{path1}"  # noqa
            code = request.query_params.get("code")
            if not code:
                logger.debug('No Code, redirecting to sso for authentication')
                return RedirectResponse(
                    self.get_auth_redirect_uri(callback_uri)
                )
            else:
                logger.debug('Received Code: %s',code)
            try:
                logger.debug('Verifying Code')
                sess_info = self.authenticate(
                    code, callback_uri, get_user_info=get_user_info
                )
                logger.debug('User Authenticated')
                
                request.__setattr__("sess_info",sess_info)
                return await view_func(request, *args, **kwargs)
            except Exception as e:
                logger.error(traceback.format_exc())
                return RedirectResponse(
                    self.get_auth_redirect_uri(callback_uri)
                )
        return decorated

    def verify_session(self,view_func):
        @wraps(view_func)
        async def decorated(
            request:Request,sessionId:str,*args,**kwargs
        ):
            logger.debug('SessionID Received to verify: %s',sessionId)
            path1="/api/login"
            callback_uri = f"{request.url.scheme}://{request.url.netloc}{path1}"
            if len(sessionId) == 0:
                return RedirectResponse(
                    self.get_auth_redirect_uri(callback_uri)
                )
            else:
                try:
                    code=self.db._get_user_session({"_id":ObjectId(sessionId)})[0]['accessToken']
                    response=self.validate_token(code)
                    logger.debug(response)
                    if response['active']:
                        logger.debug('Session State is Active, replying state to frontend')
                        request.__setattr__("sess_info",{"state":response['active']})
                        return await view_func(request,sessionId,*args,**kwargs)
                    else:
                        raise Exception('Session Expired, need to redirec to auth')
                except Exception as e:
                    logger.error(traceback.format_exc())
                    return RedirectResponse(self.get_auth_redirect_uri(callback_uri))
        return decorated