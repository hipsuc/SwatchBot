import json
from threading import Thread
import pandas as pd
from swatch import SwatchBot
from time import sleep

threads = []
tasks = []

def main() -> None:
    proxies = []
    with open("proxies.txt", "r", encoding="utf-8") as proxies_file:
        for line in proxies_file:
            buffer_proxy = line.rstrip("\n").split(":")
            proxy = buffer_proxy[2] + ":" + buffer_proxy[3] + "@" + buffer_proxy[0] + ":" + buffer_proxy[1]
            proxies.append({"http": "http://" + proxy, "https": "https://" + proxy})

    with open("config.json", "r", encoding="utf-8") as config_file:
        json_config = json.load(config_file)
        df = pd.read_csv("tasks.csv", dtype="string") # Permet de lire le fichier csv et de lancer les différentes tâches
        if len(df) != 0:
            for i in range(len(df)):
                config = {}
                config["pid"] = df.loc[i]["pid"]
                config["title"] = df.loc[i]["title"]
                config["first_name"] = df.loc[i]["first_name"]
                config["last_name"] = df.loc[i]["last_name"]
                config["email"] = df.loc[i]["email"]
                config["addy1"] = df.loc[i]["addy1"]
                config["addy2"] = df.loc[i]["addy2"]
                config["city"] = df.loc[i]["city"]
                config["zip_code"] = df.loc[i]["zip_code"]
                config["country"] = df.loc[i]["country"]
                config["phone"] = df.loc[i]["phone"]
                tasks.append(SwatchBot(config, json_config["delay"], json_config["webhook_link"], i+1, proxies))

    for task in tasks:
        t = Thread(target=task.start_task, args=())
        t.start()
        sleep(0.1)
        threads.append(t)
    for thread in threads:
        thread.join()
    threads.clear()

if __name__ == "__main__":
    main()