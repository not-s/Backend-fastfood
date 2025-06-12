from asyncio import sleep
from .send_email import send_email


async def send_welcome_email(
    email: str,
    username: str,
) -> None:
    await sleep(10)
    await send_email(
        recipient=email,
        subject="Welcome to our site",
        body=f"Dear, {username}, \n\nWelcome to our site",
    )
