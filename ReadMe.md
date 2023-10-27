Build and run the docker in a screen
```commandline
./build.sh

./run.sh
```

Setup the cronjob

```commandline
crontab -e
```

Inside the crontab:
```editorconfig
0 0 * * * bash ~/gdrive/cron-transfer-video.sh
```

