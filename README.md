# u2Spiders

# 移动设备+uiautomator2+atxserver2+weditor+mitmdump+fiddler
移动设备：真机（手机）、模拟器（夜深模拟器）
uiautomator2：安装在Ubuntu系统并连接手机进行初始化，python3.7编写自动化脚本
weditor：用于定位
mitmdump：抓取app数据，移动设备或模拟器需要设置mitmdump为代理
atxserver2：多设备监控，不用拿着每个真机去点击滑动等操作

# 打开开发者选项
设置-》我的设备-》全部参数-》MIUI版本（连续点击打开‘开发者模式’）
打开usb调试
设置-》更多设置-》开发者选项-》usb调试（打开）
电脑连接手机
此时电脑通过usb线连接手机后，可以查看手机的一些信息
adb devices
adb kill-server
打开atx
电脑终端手动打开：adb shell /data/local/tmp/atx-agent server -d

# python程序自动检测打开：
import uiautomator2 as u2# 通过手机的序列号(adb devices 查看序列号)# d = u2.connect_usb("aaf09ca9")
手机安装mitmproxy证书
把证书 mitmproxy-ca-cert.pem 拷贝到手机
设置-》WLAN-》高级设置-》安装证书-》选择证书安装即可

# 安装rethinkdb
法一：地址：https://rethinkdb.com/docs/install/ubuntu/   （安装容易出现网络问题，建议不用）
法二：下载deb手动安装：https://github.com/srh/rethinkdb/releases/tag/v2.3.6.srh.1  
     sudo dpkg -i rethinkdb_2.3.6.srh.1.0disco_amd64.deb
安装好后运行：rethinkdb

# 运行atxserver2项目
项目下载：https://github.com/openatx/atxserver2.git
安装：pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
运行：python main.py （前提是rethinkdb已经运行）
查看监控的设备：http://192.168.2.106:4000

# 安装atxserver2-android-provider
1.安装nodejs 8：curl https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
查看安装版本：nodejs -v
2.下载项目：git clone https://github.com/openatx/atxserver2-android-provider.git
cd atxserver2-android-provider/
npm install    (下载依赖的包)
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple  (下载依赖的包)
启动项目：python main.py --server http://192.168.2.106:4000（先运行atxserver2项目）
解决No module named 'humanize'：
pip install humanize -i https://pypi.tuna.tsinghua.edu.cn/simple

# 常见问题
error: no devices/emulators found
1.检查是否连上了设备或者打开了模拟器。
2.检查设备或模拟器是否打开了开发者模式。
使用模拟器不是真机
adb tcpip 5555
adb connect ip
