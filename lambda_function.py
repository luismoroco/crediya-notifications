import json
import logging

from usecase import LoanNotificationUseCase
from usecase.dto import ApplicationUpdatedDTO

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    use_case = LoanNotificationUseCase()

    records = event.get("Records", [])
    if not records:
        return {"statusCode": 400, "body": json.dumps("No Records found in the event")}

    for record in records:
        body_str = record.get("body", "")
        if not body_str:
            print("No body found in this record")
            continue

        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            print("Body is not valid JSON:", body_str)
            continue

        use_case.notify_application_updated(ApplicationUpdatedDTO.from_dict(body))

    return {"statusCode": 200, "body": json.dumps("Email sent")}
