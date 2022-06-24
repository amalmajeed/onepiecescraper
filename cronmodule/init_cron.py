# This is the entry module for initiating the cron job and running the first instance

# The cron job should run only on sundays at 5 P.M to make sure the new episode info is out
# Works only on linux machines

from crontab import CronTab
import os

# Crontab is obtained and a new job that runs every sunday is created
try:
    tab = CronTab(user=os.getlogin())
    new_job = tab.new(command='python scraper/scraper.py', comment=" This command extracts the onepiece episode to chapter map table and writes to a dataframe and uploads to mongoDB cluster")
    new_job.dow.on("SUN")
    new_job.hour.on(17)
    tab.write()
    print(" Cron job set succesfully !")
except Exception as e:
    print(f" Cron setting failed with exceptions : {e}\n")



# Once the cronjob is set - run the scraper once
print(f"Starting the scraper script !:\n")
try:
    os.system("python scraper/scraper.py")
except Exception as e:
    print(f"Scraper failed with exception: {e}\n")
