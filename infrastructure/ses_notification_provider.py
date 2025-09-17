from typing import List

import boto3
from botocore.client import BaseClient

from domain import ApplicationStatus, ApplicationUpdatedNotification
from domain.gateway import NotificationProvider


class SesNotificationProvider(NotificationProvider):

    client: BaseClient

    def __init__(self):
        self.client = boto3.client("ses", region_name="us-east-1")

    def notify_application_updated(
        self, notification: ApplicationUpdatedNotification
    ) -> None:
        payment_plan_html = ""
        if notification.applicationStatus == ApplicationStatus.APPROVED.name:
            rows = ""
            for row in notification.payment_plan:
                rows += f"""
                <tr>
                    <td>{row.row_index}</td>
                    <td>{row.total_payment:.2f}</td>
                    <td>{row.interest:.2f}</td>
                    <td>{row.principal:.2f}</td>
                    <td>{row.balance:.2f}</td>
                </tr>
                """

            payment_plan_html = f"""
            <h3>Payment Plan</h3>
            <table class="payment-table">
                <thead>
                    <tr>
                        <th>Installment</th>
                        <th>Total Payment</th>
                        <th>Interest</th>
                        <th>Principal</th>
                        <th>Remaining Balance</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            """

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
                    <p><b>Term in months:</b> {notification.term}</p>
                    
                    {payment_plan_html}
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
            content=html_content,
        )

    def _send(self, destinations: List[str], subject: str, content: str) -> None:
        self.client.send_email(
            Source="lmorocoramos@gmail.com",
            Destination={"ToAddresses": destinations},
            Message={"Subject": {"Data": subject}, "Body": {"Html": {"Data": content}}},
        )
