import uiautomator2 as u2
import time
import adbutils
import multiprocessing
from random import random, randint


class Douyin(object):
    """
    app版本：10.1.0
    真机测试：小米 5S
    抓取 推荐 页面抖音视频信息和个人主页信息
    """

    def __init__(self, serial="aaf09ca9"):
        self.d = u2.connect_usb(serial)
        self.start_app("com.ss.android.ugc.aweme")
        self.size = self.get_windowsize()
        self.handle_watcher()
        # 初始运行时间
        self.t0 = time.perf_counter()

    def start_app(self, package_name):
        self.d.app_start(package_name)

    def stop_app(self, package_name):
        self.d.watcher.stop()
        self.d.app_stop(package_name)
        self.d.app_clear(package_name)

    def stop_time(self, t):
        """停止爬虫"""
        # 时间是秒
        if time.perf_counter() - self.t0 > t:
            return True

    def handle_watcher(self):
        """监视器"""
        # 上滑查看更多视频
        self.d.watcher.when('//*[@text="滑动查看更多"]').call(self.handle_swipe)
        # 启动监控器
        self.d.watcher.start(interval=1)

    def get_windowsize(self):
        return self.d.window_size()

    def handle_swipe(self):
        # 滑动
        x1 = int(self.size[0] * random())
        y1 = int(self.size[1] * randint(6, 9)*0.1)
        y2 = int(self.size[1] * randint(1, 5)*0.1)
        self.d.swipe(x1, y1, x1, y2)

    def swipe_douyin(self):
        # 来判断是否正常的进入到了视频页面，网络情况不好也包含在内了
        if self.d(resourceId="com.ss.android.ugc.aweme:id/yy", text="发现").exists(timeout=20):
            while True:
                # 到规定的时间停止循环
                if self.stop_time(60*60):
                    self.stop_app("com.ss.android.ugc.aweme")
                    return

                # 查看是不是正常的发布者,看他的头像上有没有加号
                if self.d(resourceId="com.ss.android.ugc.aweme:id/u0").exists:
                    # 是正常的发布者，点击 @xxx 进入发布者页面
                    try:
                        self.d(resourceId="com.ss.android.ugc.aweme:id/ai").click()
                        # 返回视频推荐页面
                        self.d(resourceId="com.ss.android.ugc.aweme:id/et").click(timeout=3)
                        print('正常进入个人信息页')
                    except:
                        pass
                elif self.d(resourceId="com.ss.android.ugc.aweme:id/yy", text="发现"):
                    # 可能是广告
                    self.handle_swipe()
                    print('可能广告')

                if self.d(resourceId="com.ss.android.ugc.aweme:id/yy", text="发现").exists:
                    # 正常的一个滑动
                    self.handle_swipe()
                    print('正常下一个视频')


def get_devices():
    # 获取到当前操作系统中所连接的移动设备,serial num
    return [d.serial for d in adbutils.adb.device_list()]


def handle_device(serial):
    d = Douyin(serial)
    # 模拟滑动抖音短视频
    d.swipe_douyin()


def main():
    # 多进程启动u2去控制移动设备
    for i in range(len(get_devices())):
        serial = get_devices()[int(i)]
        p = multiprocessing.Process(target=handle_device, args=(serial,))
        # 启动进程
        p.start()


if __name__ == '__main__':
    # d = Douyin()
    # d.swipe_douyin()
    # print(get_devices())
    main()
