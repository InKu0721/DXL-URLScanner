import socket
import argparse
import progressbar
import concurrent.futures
import art
import ipaddress


# 清理URL函数，用于移除可能存在的"http://"或"https://"前缀
def clean_url(url):
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    return url


# 获取IP地址或主机名的函数
def get_ip_address(url):
    try:
        ip = ipaddress.ip_address(url)  # 尝试将输入解析为IP地址对象
        return str(ip)  # 如果成功，返回IP地址字符串表示
    except ValueError:
        try:
            ip_address = socket.gethostbyname(url)  # 如果无法解析为IP地址，尝试解析为主机名
            return ip_address  # 返回主机名对应的IP地址
        except socket.gaierror:
            print(f"Could not resolve host: {url}")  # 如果无法解析主机名，打印错误消息并退出
            exit(1)


# 扫描单个端口的函数
def scan_port(ip_address, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # 设置套接字连接超时时间为1秒
            result = s.connect_ex((ip_address, port))  # 尝试连接到目标IP地址和端口
            if result == 0:  # 如果连接成功，返回端口号
                return port
    except socket.error:
        pass
    return None  # 如果出现错误或连接失败，返回None


# 扫描一定范围内的端口的函数
def scan_ports(ip_address, num_threads, min_port, max_port):
    open_ports = []
    ports_to_scan = range(min_port, max_port + 1)  # 生成要扫描的端口范围
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(scan_port, ip_address, port) for port in ports_to_scan]  # 创建线程任务列表
        with progressbar.ProgressBar(max_value=len(ports_to_scan)) as bar:
            for i, future in enumerate(concurrent.futures.as_completed(futures)):  # 迭代处理线程任务
                result = future.result()
                if result is not None:
                    open_ports.append(result)
                bar.update(i)  # 更新进度条
    return open_ports  # 返回开放的端口列表


# 获取端口对应的服务名称的函数
def get_service_name(port):
    try:
        service_name = socket.getservbyport(port)  # 尝试获取端口对应的服务名称
        return service_name  # 返回服务名称
    except OSError:
        return "Unknown"  # 如果无法获取服务名称，返回"Unknown"


if __name__ == "__main__":
    # 打印字符画函数
    def print_ascii_art():
        ascii_art = art.text2art("DXL URLscanner")  # 创建字符画
        print(ascii_art)  # 打印字符画


    print_ascii_art()  # 调用打印字符画函数

    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="DXL URLscanner - 作者：東雪蓮Sec")
    # 添加命令行参数
    parser.add_argument("-u", "--url", required=True, help="要扫描的URL或IP地址")
    parser.add_argument("-t", "--threads", type=int, default=4, help="线程数（最大648）")
    parser.add_argument("-min", type=int, default=1, help="最小扫描端口")
    parser.add_argument("-max", type=int, default=65535, help="最大扫描端口")
    args = parser.parse_args()  # 解析命令行参数

    # 限制线程数不超过648
    num_threads = min(args.threads, 648)
    url = args.url
    url = clean_url(url)  # 清理URL
    host_name = url.split('/')[0]  # 提取主机名

    # 获取IP地址
    ip_address = get_ip_address(host_name)
    print(f"{host_name}的IP地址: {ip_address}")

    # 扫描端口
    open_ports = scan_ports(ip_address, num_threads, args.min, args.max)

    if open_ports:
        print("开放的端口:")
        for port in open_ports:
            service_name = get_service_name(port)
            print(f"端口 {port}（{service_name}）是开放的")
    else:
        print("未找到开放的端口")
