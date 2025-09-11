import json

from usecase import LoanNotificationUseCase
from usecase.dto.ApplicationUpdatedDTO import ApplicationUpdatedDTO


def lambda_handler(event, context):
    useCase = LoanNotificationUseCase()

    records = event.get('Records', [])
    if not records:
        return {
            'statusCode': 400,
            'body': json.dumps('No Records found in the event')
        }

    for record in records:
        body_str = record.get('body', '')
        if not body_str:
            print("No body found in this record")
            continue

        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            print("Body is not valid JSON:", body_str)
            continue

        useCase.notify_application_updated(
            ApplicationUpdatedDTO(**body)
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent')
    }
