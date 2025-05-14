import logging
import time
from app.core.age_group_api import AgeGroupAPIClient
from app.core.constants import EnrollmentStatus
from app.core.db import DatabaseProvider
from app.core.rabbitmq import RabbitMQProvider

from app.repositories.enrollment import EnrollmentRepository
from app.schemas.filters import EnrollmentFilter


logging.basicConfig(
    filename="processor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def process_enrollment(ch, method, properties, body):
    enrollment_id = body.decode()
    logger.info(f"Enrollment ID {enrollment_id}: Start processing.")

    db = DatabaseProvider.get_database()
    repository = EnrollmentRepository(db)

    time.sleep(2)

    enrollment = repository.get(enrollment_id)

    if not enrollment:
        logger.error(f"Enrollment ID {enrollment_id}: Enrollment not found.")
        ch.basic_nack(delivery_tag=method.delivery_tag)
        return

    age_group_api_client = AgeGroupAPIClient()
    try:
        age_groups = age_group_api_client.get_age_groups_by_age(enrollment.age)
    except Exception as e:
        logger.error(f"Enrollment ID {enrollment_id}: Error consuming age group api. Error: {str(e)}")
        repository.update_status(
            enrollment_id=enrollment.id,
            status=EnrollmentStatus.REFUSED,
        )
        ch.basic_nack(delivery_tag=method.delivery_tag)
        return

    if not age_groups:
        logger.error(f"Enrollment ID {enrollment_id}: There's no age group available for age {enrollment.age}.")
        repository.update_status(
            enrollment_id=enrollment.id,
            status=EnrollmentStatus.REFUSED,
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    logger.info(f"Enrollment ID {enrollment_id}: Accepted.")
    repository.update_status(
        enrollment_id=enrollment.id,
        status=EnrollmentStatus.ACCEPTED,
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    provider = RabbitMQProvider()
    channel = provider.get_channel()

    channel.basic_consume(
        queue=provider.get_queue_name(), on_message_callback=process_enrollment,
    )

    logger.info(f"Start processing in queue enrollments.")
    channel.start_consuming()


if __name__ == '__main__':
    main()
