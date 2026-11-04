from datetime import datetime

def enrolment_is_open(closes_at: datetime, now: datetime) -> bool:
    return now < closes_at