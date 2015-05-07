# -*- coding: utf-8 -*-

import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd

event_list = ["222", "333", "333oh", "444", "555"]


def crawl_jc(event_list):
    n_sanka = defaultdict(int)
    n_atari = defaultdict(int)

    for event in event_list:
        i_contest = 1
        while True:
            print("{0} {1}回目".format(event, i_contest))
            results_url = "http://japancontest.net/result/contest/{0}/{1}/".format(event, i_contest)
            f = urlopen(results_url)
            soup = BeautifulSoup(f, "lxml")
            lines = list(map(str, soup.find_all('tr')))
            if len(lines) < 3:
                break
            for line in lines:
                pattern = r'<a href="/result/name/.+?">(.+?)</a>'
                m = re.search(pattern, line)
                if m:
                    name = m.group(1)
                    n_sanka[name] += 1
                else:
                    continue
                if line.find("atari.png") > -1:
                    n_atari[name] += 1
                    print("当選: {0} ({1}回目)".format(name, n_atari[name]))
            i_contest += 1
    return (n_sanka, n_atari)


def main():
    n_sanka, n_atari = crawl_jc(event_list)
    results = pd.DataFrame(columns=["name", "n_sanka", "n_atari", "rate"])
    for name in n_sanka.keys():
        rate = n_atari[name] / n_sanka[name]
        record = pd.Series([name, n_sanka[name], n_atari[name], rate],
                           index=list(["name", "n_sanka", "n_atari", "rate"]))
        results = results.append(record, ignore_index=True)
    results = results.sort(columns="n_atari", ascending=False)
    results.to_csv('results.csv', index=False)


if __name__ == '__main__':
    main()