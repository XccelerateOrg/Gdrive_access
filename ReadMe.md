build and run the docker in a screen
```commandline
./build.sh

./run.sh
```

Once inside the container:

setup the cronjob

```commandline
crontab -e
```

Inside the crontab:
```editorconfig
0 0 * * * /gdrive/cron-transfer-video.sh
```

```commandline
run-app.sh
```
