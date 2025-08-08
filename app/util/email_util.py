from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from pydantic import EmailStr
from typing import List

# Create the connection configuration from your settings
conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_collaboration_invite_email(
    recipient_email: EmailStr,
    game_name: str,
    role: str,
    game_id: str
):
    """
    Sends an invitation email to a new collaborator.
    """
    # This is the link to your frontend game management page
    collaboration_link = f"{settings.FRONTEND_URL}/admin/games/{game_id}"

    html_content = f"""
    <html>
        <body>
            <h2>You've been invited to collaborate!</h2>
            <p>Hello,</p>
            <p>
                You have been invited to collaborate on the game <strong>{game_name}</strong>
                with the role of <strong>{role}</strong>.
            </p>
            <p>Click the link below to view the game:</p>
            <a href="{collaboration_link}" style="padding: 10px 20px; color: white; background-color: #007bff; text-decoration: none; border-radius: 5px;">
                Go to Game
            </a>
            <p>Thank you!</p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject=f"Invitation to Collaborate on: {game_name}",
        recipients=[recipient_email],
        body=html_content,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

async def send_team_invitation_email(
    recipient_email: EmailStr,
    team_name: str,
    game_name: str,
    game_join_code: str
):
    """
    Sends an invitation email to a new player who has been added to a team.
    """
    # This is the link to your frontend's join page
    join_link = f"{settings.FRONTEND_URL}/join/{game_join_code}"

    html_content = f"""
    <html>
        <body>
            <h2>You've been added to a team!</h2>
            <p>Hello,</p>
            <p>
                You have been added to the team <strong>{team_name}</strong>
                for the treasure hunt: <strong>{game_name}</strong>.
            </p>
            <p>If you haven't created your team yet, you can use the link below to join the game:</p>
            <a href="{join_link}" style="padding: 10px 20px; color: white; background-color: #007bff; text-decoration: none; border-radius: 5px;">
                Join Game
            </a>
            <p>Good luck!</p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject=f"You've been added to team '{team_name}' for {game_name}",
        recipients=[recipient_email],
        body=html_content,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
