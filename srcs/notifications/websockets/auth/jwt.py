from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.state import token_backend


async def validate_jwt_and_get_user_id(token):
    try:
        UntypedToken(token)

        decoded_data = token_backend.decode(token, verify=True)
        # print(decoded_data)
        user_id = decoded_data.get('user_id')

        return user_id
    except (InvalidToken, TokenError) as e:
        print("Invalid Token: ", e)
        return None
