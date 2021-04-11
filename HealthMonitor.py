import datetime
import logging

import feeding_cache
import food
from tools import run_periodically
from mailing import MailingService


logger = logging.getLogger(__name__)


FEEDING_INTERVAL = 10
HEALTH_CHECK_INTERVAL = 10


class HealthMonitor:

    def __init__(self, feeding_interval, health_check_interval):
        print('ctor')
        self.warning_sent = False
        self.feeding_interval = feeding_interval
        self.health_check_interval = health_check_interval
        self.mailing_service = MailingService()
        self.alerts_email_subscriber = 'dy@gmail.com'

    @property
    def last_feeding_time(self) -> datetime.datetime:
        """Get the last time the cat has been fed"""
        return datetime.datetime.strptime(feeding_cache.get_feeding_data(), "%m/%d/%Y, %H:%M:%S")

    def update_last_feeding_time(self, last_feeding_time: datetime.datetime):
        """
        Set last feeding time in cache

        Args:
            last_feeding_time: the time of the last feeding

        Returns:
            None
        """
        feeding_cache.update_feeding_data(last_feeding_time.strftime("%m/%d/%Y, %H:%M:%S"))

    @property
    def cat_has_been_fed(self) -> bool:
        """Has the cat been fed in the recent feeding interval?"""
        return (datetime.datetime.now() - self.last_feeding_time).total_seconds() > self.feeding_interval * 60

    def check_for_new_food(self):
        print('check for new food')
        last_added_food = food.CatFood.get_last_added_cat_food()
        new_feeding_timestamp = last_added_food.timestamp
        self.update_last_feeding_time(new_feeding_timestamp)

    def send_warning_email(self):
        self.mailing_service.send_message(self.alerts_email_subscriber, 'ALERT! The cat is hungry!',
                                              'The cat han\'t been fed recently. Please feed fast!!!')

    def send_back_to_normal_email(self):
        self.mailing_service.send_message(self.alerts_email_subscriber, 'Back To Normal',
                                              'The cat has been fed again! Thanks!')

    def send_feeding_alerts_in_needed(self):
        print('send_feeding_alerts_in_needed')
        """Our cat doesn't die if not fed but the alert will remind once if the cat hasn't been fed recently"""
        if self.cat_has_been_fed:
            print('send_feeding_alerts_in_needed - cat has been fed')
            logger.info("cat is well")
            if self.warning_sent:
                self.send_back_to_normal_email()
        else:
            print('send_feeding_alerts_in_needed - cat was NOTTTTTT fed')
            if not self.warning_sent:
                self.send_warning_email()


if __name__ == '__main__':
    health_checker = HealthMonitor(FEEDING_INTERVAL, HEALTH_CHECK_INTERVAL)
    # Example code. Both functions run forever
    # run_periodically(health_checker.check_for_new_food, 20)
    # run_periodically(health_checker.send_feeding_alerts_in_needed, HEALTH_CHECK_INTERVAL)
