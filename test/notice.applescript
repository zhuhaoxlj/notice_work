-- 设置通知的属性
set notificationText to "这是通知文本"
set notificationTitle to "通知标题"
set notificationSubtitle to "通知副标题"
-- 可以更改为其他系统提供的声音名称
set notificationSound to "Glass" 
-- 替换为您自己的图标文件的路径
set iconPath to "/Users/markgosling/Documents/100-Project/02-Python/MyScript/notice.png" 

-- 创建通知
display notification notificationText with title notificationTitle subtitle notificationSubtitle sound name notificationSound ¬
  image from POSIX file iconPath
