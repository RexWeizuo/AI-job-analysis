# Power Automate脚本文件使用说明
本脚本划为两个模块，一是岗位基本信息提取（含链接），二是遍历链接，提取岗位详细信息。
## 岗位基本信息提取

- 从外部CSV文件中读取岗位关键字：请在首行的```File.ReadFromCSVFile.ReadCSV CSVFile: $'''C:\\Users\\zdong\\Desktop\\岗位关键字.csv''' ```中，将关键字csv修改成你的路径。
- 启动Edge
- 循环关键字列表
    - 随机等待模块：请在```Variables.GenerateRandomNumber.RandomNumber MinimumValue: 1 MaximumValue: 3 RandomNumber=> RandomNumber```的```MinimumValue: 1 MaximumValue: 3```中修改等待时间的范围
    - 模拟搜索关键字
    - 检测弹窗并叉掉
    - 提取前两页数据
    - 将提取的数据追加至外部动态csv表（本表在后期处理完后会自动删除）
- 关闭浏览器
- 运行powershell脚本：激活虚拟环境并调用```dupi.py```脚本。py脚本作用：删除空值与重复值，更新列名，并将处理后的基本信息保存为bossbase/boss_月日时分.csv，删除动态csv表。

## 岗位详细信息提取
- 运行powershell脚本：在bossbase中检测更新日期最新的boss_*.csv文件，输出其文件完整路径。
- 读取该文件
- 提取文件的链接列作为列表
- 启动Edge
- 循环提取数据
- 运行powershell脚本：激活虚拟环境并调用```plus.py```脚本。py脚本作用：删除boss_*.csv中的链接列，将读取出的新内容横向拼接，更新列名并保存为boin_月日时分.csv
- 运行powershell脚本：激活虚拟环境并调用```duplus.py```脚本。py脚本作用：将boin_月日时分.csv合并进总的boin.csv，在总文件中删除重复值。
- 运行powershell脚本：获取今天的月日，进入git仓库文件夹，提交并推送文件。
- 打开CMD会话
- 发送关机指令

## 注意事项
- 文中提到的python脚本在```/powerautomate/utils/```文件夹下。
- boss_*.csv、py文件等中间文件没有保存在本仓库中，各类路径需自行修改