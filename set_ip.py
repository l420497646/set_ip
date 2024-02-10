import subprocess
import wmi


def get_ip_type():
    wmi_service = wmi.WMI()
    configs = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    for config in configs:
        if config.DHCPEnabled:
            return "dhcp"
    return "static"


def set_static_ip(ip, mask, gateway, dns1, dns2):
    try:
        command1 = (f"netsh interface ip set address name=以太网 source=static address={ip} mask={mask} "
                    f"gateway={gateway}")
        command2 = f"netsh interface ip set dns name=以太网 source=static addr={dns1} register=primary validate=no"
        command3 = f"netsh interface ip add dns name=以太网 {dns2} index=2 validate=no"

        subprocess.run(["powershell.exe", "-Command", command1], shell=True, check=True)
        subprocess.run(["powershell.exe", "-Command", command2], shell=True, check=True)
        subprocess.run(["powershell.exe", "-Command", command3], shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"设置静态IP时出错：{e.stderr}")


def set_dhcp():
    try:
        command1 = "netsh interface ip set address name=以太网 source=dhcp"
        command2 = "netsh interface ip set dns name=以太网 source=dhcp"
        subprocess.run(["powershell.exe", "-Command", command1], shell=True, check=True)
        subprocess.run(["powershell.exe", "-Command", command2], shell=True, check=True)
        print("切换到DHCP成功！")
    except subprocess.CalledProcessError as e:
        print(f"切换到DHCP时出错：{e.stderr}")


if __name__ == "__main__":
    static_ip = "192.168.1.120"
    mask = "255.255.255.0"
    static_gateway = "192.168.1.11"
    static_dns1 = "114.114.114.114"
    static_dns2 = "8.8.8.8"

    mode = get_ip_type()
    print("当前模式为：" + mode)
    if mode == "static":
        print("设置为dhcp模式，请稍后")
        set_dhcp()
    elif mode == "dhcp":
        print("设置为static模式，请稍后")
        print("IP:" + static_ip + "/" + mask + " gateway:" + static_gateway)
        print("dns1:" + static_dns1 + " dns2:" + static_dns2)
        set_static_ip(static_ip, mask, static_gateway, static_dns1, static_dns2)
    else:
        print("模式错误")

    input("按下回车键以退出...")
