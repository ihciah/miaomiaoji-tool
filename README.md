# 喵喵机蓝牙API By ihciah

### 依赖

`pybluez` 蓝牙API需要(树莓派上折腾这东西踩了挺多坑

`twisted, pyopenssl` 微信接口脚本需要

`cv2, numpy` 图像转换工具需要

### 建立连接

`BtManager()` 参数留空会搜索附近可用的喵喵机并连接

`BtManager("69:68:63:69:61:68")` 附加指定MAC会跳过搜索过程直接连接设备，更省时间

### 打印图像

从API看该机器只能输入二值图像进行打印，所以文本转图片是在客户端完成的。

打印的图像格式为二进制数据，每一位表示黑(1)或白(0)，每行384个点。

```python
mmj = BtManager()
mmj.sendImageToBt(img)
mmj.disconnect()
```

### 其他杂项

`registerCrcKeyToBt(key=123456)` 更改通信CRC32 KEY(不太懂这么做是为了啥,讲道理监听到这个包就能拿到key的)

`sendPaperTypeToBt(paperType=0)` 更改纸张类型(疯狂卖纸呢)

`sendPowerOffTimeToBt(poweroff_time=0)` 更改自动关机时间

`sendSelfTestToBt()` 打印自检页面

`sendDensityToBt(density)` 设置打印密度

`sendFeedLineToBt(length)` 控制打印完后的padding

`queryBatteryStatus()` 查询剩余电量

`queryDensity()` 查询打印密度

`sendFeedToHeadLineToBt(length)` 不太懂和 `sendFeedLineToBt` 有什么区别，但是看起来都是在打印后调用的。

`queryPowerOffTime()` 查询自动关机时间

`querySNFromBt()` 查询设备SN

其实还有挺多操作的，有兴趣的看着`const.py`猜一猜好了。

### 图像工具

`ImageConverter.image2bmp(path)` 任意图像到可供打印的二进制数据转换
 
`TextConverter.text2bmp(text)` 指定文字到可供打印的二进制数据转换

### 微信公众平台工具

两个小脚本，用来实现发送图片给微信公众号后自动打印。

`wechat.php` 用于VPS接收腾讯数据，默认只允许指定用户打印。

`printer_server.py` 放置于树莓派等有蓝牙的靠近喵喵机的机器上运行，可以使用`tinc`等建立VPN以供VPS直接访问。

### 吐槽

这玩意就不能增加一个多次打印的功能吗？以较低温度多次打印再走纸，应该可以实现打印灰度图的。

逆了好久的固件也没搞出来啥东西，真是菜。希望有大佬能告诉我一点人生的经验。

顺便丢两个芯片型号: `NUC123LD4BN0`, `STM32F071CBU6`，似乎是Cortex-M0。

PS: 本代码仅供非盈利用途，如用于商业用途请另请高明。
