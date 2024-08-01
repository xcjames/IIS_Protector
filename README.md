# IIS_Protector
这个python程序可以分析IIS日志文件，并拦截访问量超过一定数量的恶意IP，您可以自行定制。
<br>
This python program analyze IIS log file, and block the malicious IP that have visits exceeds a certain amount, which can be customized by you.
<br>

## 如何使用 How to use
### 1. 设置好配置文件：Set the config files
path.conf 文件中有四项:<br>
(1)iis_log_path=你的IIS log文件夹路径  <br>
(2)start_line_num=指定第几行，从log文件这一行开始向下读取。  <br>
(3)now_log_name=检测到文件夹中最新编辑了的log文件的文件名  <br>
(4)max_visit_one_day=对某个IP允许的最大访问次数，超出此次数则立刻将IP加入防火墙阻止访问。 <br>

history_disabled_ip.conf记录了所有已被阻止访问的IP。会自动更新，不需要手动编辑。

There are four items in the path.conf file:<br>
(1)iis_log_path=your IIS log folder path <br>
(2)start_line_num=specify the line number, start reading from this line of the log file. <br>
(3)now_log_name=the name of the most recently edited log file in the folder <br>
(4)max_visit_one_day=the maximum number of visits allowed to a certain IP. If an IP visit times exceed this number, the IP will be immediately added to the firewall to block access. <br>

history_disabled_ip.conf records all IPs that have been blocked. It will be automatically updated and does not need to be manually edited.

### 2. 运行 Run
`python ipdisable.py`
