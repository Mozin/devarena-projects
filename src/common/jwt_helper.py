import datetime

from flask_jwt_extended import create_access_token, get_jwt_identity

from src import jwt


def create_token_obj_bundle(user):
    expires_time = datetime.timedelta(days=1)
    access_token = create_access_token(identity=user, expires_delta=expires_time)
    ret = {'accessToken': access_token, 'userObj': {k:v for k,v in user.__dict__.items() if not k in ["_sa_instance_state", "password"]}}
    return ret


@jwt.user_identity_loader
def user_identity_loader(user):
    return user.id

def get_user_identity():
    return get_jwt_identity()


