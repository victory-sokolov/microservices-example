import json


def post_user_data(app):
    return app.post(
        "/users",
        data=json.dumps({
            "username": "viktor",
            "email": "viktorsokolov.and@gmail.com"
        }),
        content_type="application/json",
    )
