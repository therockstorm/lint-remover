from __future__ import print_function
from datetime import datetime
import json
import requests


BASE_URL = "https://getpocket.com/v3"
THREE_YEARS = 365 * 3

class LintRemover(object):
    def __init__(self):
        self.headers = {"X-Accept": "application/json",
                        "Content-Type": "application/json; charset=UTF8"}
        self.key = ""
        self.token = ""
        self.http = requests

    def delete_articles_older_than(self, days):
        archived_articles = self._get_archived_articles()
        old_articles = []
        now = datetime.now()
        for _key, article in archived_articles.iteritems():
            delta = now - datetime.fromtimestamp(float(article["time_added"]))
            if article["favorite"] == "0" and delta.days > days:
                old_articles.append({"action": "delete", "item_id": article["item_id"]})

        self._delete_articles(old_articles)

    def _get_archived_articles(self):
        data = {"consumer_key": self.key,
                "access_token": self.token,
                "state": "archive"}

        res = self.http.post("{0}/get".format(BASE_URL),
            headers=self.headers, data=json.dumps(data)).json()

        if res["error"]:
            print(res["error"])
            return {}

        return res["list"]

    def _delete_articles(self, articles):
        print("Deleting {0} articles...".format(len(articles)))

        data = {"consumer_key": self.key,
                "access_token": self.token,
                "actions": articles}

        delete_res = self.http.post("{0}/send".format(BASE_URL),
            headers=self.headers, data=json.dumps(data)).json()

        print(delete_res)


if __name__ == "__main__":
    LintRemover().delete_articles_older_than(THREE_YEARS)
