from typing import List

from botocore.client import BaseClient
import boto3

from domain.ApplicationUpdatedNotification import ApplicationUpdatedNotification
from domain.gateway import NotificationProvider

class SESNotificationProvider(NotificationProvider):

    client: BaseClient

    def __init__(self):
        self.client = boto3.client('ses', region_name='us-east-1')

    def notify_application_updated(self, notification: ApplicationUpdatedNotification) -> None:
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #0056d2;
                    color: white;
                    padding: 15px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                }}
                .content {{
                    padding: 20px;
                    font-size: 16px;
                    color: #333333;
                }}
                .status-box {{
                    background-color: #f1f1f1;
                    padding: 10px;
                    margin: 20px 0;
                    font-weight: bold;
                    text-align: center;
                }}
                .footer {{
                    font-size: 12px;
                    color: #999999;
                    text-align: center;
                    padding: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">Loan Notification</div>
                <div class="content">
                    <p>Hello,</p>
                    <p>Your application with ID <b>{notification.applicationId}</b> has been processed.</p>

                    <div class="status-box">
                        Application status: {notification.applicationStatus}
                    </div>

                    <p><b>Requested amount:</b> {notification.amount}</p>
                    <p><b>Term in months:</b> {notification.amount}</p>

                </div>
                <div class="footer">
                    © CreditYa 2025.
                </div>
            </div>
        </body>
        </html>
        """

        self._send(
            destinations=[notification.email],
            subject="Loan Request Decision",
            content=html_content
        )

    def _send(self, destinations: List[str], subject: str, content: str) -> None:
        self.client.send_email(
            Source='lmorocoramos@gmail.com',
            Destination={
                'ToAddresses': destinations
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Html': {
                        'Data': content
                    }
                }
            }
        )
