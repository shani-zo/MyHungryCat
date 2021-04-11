import time

from tools import run_periodically
import feeding_data


FEEDING_INTERVAL = 15
HEALTH_CHECK_INTERVAL = 15


class HealthMonitor:

    def __init__(self, feeding_interval, health_check_interval):
        self.warning_sent = False
        self.feeding_interval = feeding_interval
        self.health_check_interval = health_check_interval

    @property
    def last_feeding_time(self) -> int:  # TODO
        """Get the last time the cat has been fed"""
        return 1

    def update_last_feeding_time(self, last_feeding_time: float):
        """
        Set last feeding time in cache

        Args:
            last_feeding_time: the time of the last feeding

        Returns:
            None
        """
        feeding_data.update_feeding_data(str(last_feeding_time))

    @property
    def cat_has_been_fed(self) -> bool:
        """Has the cat been fed in the recent feeding interval?"""
        return time.time() - self.last_feeding_time > self.feeding_interval

    def check_for_new_food(self):  # TODO
        new_food_timestamp = 0
        self.update_last_feeding_time(new_food_timestamp)

    def send_warning(self):  # SHOULD CHANGE TO EVENT? TODO
        pass

    def send_back_to_normal(self):  # TODO
        pass

    def check_feeding_state(self):
        if self.cat_has_been_fed:
            if self.warning_sent:
                self.send_back_to_normal()
        else:
            if not self.warning_sent:
                self.send_warning()


if __name__ == '__main__':
    health_checker = HealthMonitor(FEEDING_INTERVAL, HEALTH_CHECK_INTERVAL)
    run_periodically(health_checker.check_for_new_food(), 1)
    run_periodically(health_checker.check_feeding_state(), HEALTH_CHECK_INTERVAL)

