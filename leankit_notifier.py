import requests
import json
import time
import datetime

import config


class LeankitNotifier:

    def __init__(self, account_name, board_id, lane_id, base64_authorization, max_allowed_size):
        """
            base64_authorization is a base64 encoding of '<username>:<password>'
        """
        self.account_name = account_name
        self.board_id = board_id
        self.lane_id = lane_id
        self.base64_authorization = base64_authorization
        self.max_allowed_size = max_allowed_size

    def print_report(self):
        url = "https://{}.leankit.com/kanban/api/boards/{}".format(self.account_name, self.board_id)
        headers = {"Authorization": "Basic {}".format(self.base64_authorization)}

        response = requests.get(url, headers=headers)

        result = json.loads(response.text)

        development_lane = [lane for lane in result["ReplyData"][0]["Lanes"] if lane["Id"] == self.lane_id]
        if len(development_lane) > 0:
            development_lane = development_lane[0]
        else:
            print("ERROR: Lane not found")
            exit(1)

        print("Checking '{}' lane (id: {})".format(development_lane["Title"], development_lane["Id"]))

        lane_cards = [card for card in development_lane["Cards"]]

        for card in lane_cards:
            print("> {} ({}):".format(card["Title"], ",".join(self._get_assigned_users(card))))
            if not self._has_assigned_users(card):
                print("  - Not assigned")
            if not self._is_estimated(card):
                print("  - Not estimated")
            if self._is_estimated(card) and self._is_too_big(card):
                print("  - Estimation is too big (max. {})".format(self.max_allowed_size))
            if not self._is_scheduled(card):
                print("  - Not scheduled")
            if self._is_scheduled(card):
                if self._is_overdue(card):
                    print("  - Overdue")
                if self._is_wrongly_scheduled(card):
                    print("  - Due date looks too far away")

    def _is_estimated(self, card):
        return card["Size"] > 0

    def _is_too_big(self, card):
        return card["Size"] > self.max_allowed_size

    def _is_scheduled(self, card):
        return card["DueDate"] != ""

    def _has_start_date(self, card):
        return card["StartDate"] != ""

    def _is_wrongly_scheduled(self, card):
        if not self._is_scheduled(card):
            return False
        if not self._has_start_date(card):
            return False

        threshold_days = 2
        threshold = datetime.timedelta(days=threshold_days)

        start_date = self._get_start_date(card)
        end_date = self._get_due_date(card)
        return (end_date - start_date).days > card["Size"] + threshold_days

    def _is_overdue(self, card):
        if not self._is_scheduled(card):
            return False
        card_date = self._get_due_date(card)
        current_date = datetime.date.fromtimestamp(time.time())
        return current_date > card_date

    def _has_assigned_users(self, card):
        return len(card["AssignedUsers"]) > 0

    def _get_assigned_users(self, card):
        return [user["EmailAddress"] for user in card["AssignedUsers"]]

    def _get_due_date(self, card):
        return self._card_date(card["DueDate"])

    def _get_start_date(self, card):
        return self._card_date(card["StartDate"])

    def _card_date(self, card_date_field):
        card_date_fragments = card_date_field.split("/")
        return datetime.date(int(card_date_fragments[0]), int(card_date_fragments[1]), int(card_date_fragments[2]))


def main():
    site_builder = LeankitNotifier(config.account_name, config.board_id, config.lane_id, config.base64_authorization,
                                   config.max_allowed_size)
    site_builder.print_report()

if __name__ == '__main__':
    main()
