简单写了一个关于url的扫描器，可以扫描出ip以及开发端口的相应服务

usage: DXLurlscanner.py [-h] -u URL [-t THREADS] [-min MIN] [-max MAX]

DXL URLscanner - 作者：東雪蓮Sec

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     要扫描的URL或IP地址
  -t THREADS, --threads THREADS
                        线程数（最大648）
  -min MIN              最小扫描端口
  -max MAX              最大扫描端口
