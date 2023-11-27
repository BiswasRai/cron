from celery import shared_task
from .services.student_service import generate_fake_student_data, create_students
from celery.contrib.abortable import AbortableTask
from celery.schedules import timedelta

@shared_task(bind=True, base=AbortableTask, max_retries=1)
def celery_add_students(self, num_students):
    try:
        student_data = generate_fake_student_data(num_students)
        success = create_students(student_data)

        return success
    except Exception as exc:
        # create a handler function for exceptional handling and can integrate sms for alerting
        countdown = 1 ** self.request.retries
        self.retry(exc=exc, countdown=countdown)
        return {"error while adding students": str(exc)}