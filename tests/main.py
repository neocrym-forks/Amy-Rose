from sanic import Sanic
from sanic.response import text

from amyrose.core.authentication import register, verify_account, authentication_middleware, login
from amyrose.core.utils import send_verification_code
from amyrose.lib.tortoise import tortoise_init

app = Sanic("AmyRose example")


@app.middleware('request')
async def print_on_request(request):
    authentication_middleware(request)


@app.post("/register")
async def on_register(request):
    account, session = await register(request)
    await send_verification_code(account, session)
    response = text('Registration successful')
    response.cookies[session.token_name] = session.token
    return response


@app.post("/login")
async def on_login(request):
    account, session = await login(request)
    response = text('Login successful')
    response.cookies[session.token_name] = session.token
    return response


@app.post("/verify")
async def on_verify(request):
    await verify_account(request)
    return text('Verification successful')


if __name__ == "__main__":
    app.add_task(tortoise_init())
    app.run(host="0.0.0.0", port=8000)