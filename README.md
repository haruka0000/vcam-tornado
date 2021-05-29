# vcam-tornado
This program outputs an HTML canvas to a fake camera using Javascript and Python server.

## Environment
Linux OpenSUSE tumbleweed

Python 3.9.5

```
$ pip install -r requirements.txt
```


## Prepare v4l2loopback
```
$ git clone https://github.com/umlaeute/v4l2loopback.git
$ cd v4l2loopback
$ make && sudo make install
$ sudo depmod -a
$ echo "options v4l2loopback video_nr=42 exclusive_caps=1" | sudo tee -a /etc/modprobe.d/v4l2loopback.conf
$ echo v4l2loopback | sudo tee -a /etc/modules-load.d/modules.conf
$ sudo systemctl restart systemd-modules-load.service
```
```
$ ls /dev/video*
/dev/video0  /dev/video42
```

## Run
```
$ python server.py
```

Open [http://localhost:8888/](http://localhost:8888/)

```
$ ffplay /dev/video42
```
