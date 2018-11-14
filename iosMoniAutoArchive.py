#!/usr/bin/env python
#coding=utf-8
import subprocess
import os

import shutil
import requests
import webbrowser
import smtplib
from email.mime.text import MIMEText

#项目名称
PRODUCT_NAME = ""
#版本号
APP_VERSION = ""
#打出的xx.ipa包根目录
EXPECT_OPTION_PATH = "~/Desktop/iosMoniArchive/"
RELEASE_TYPE = "Release"

#导出包路径
IPA_EXPORTPATH = EXPECT_OPTION_PATH + APP_VERSION + "/"
BUILD_PATH = IPA_EXPORTPATH + PRODUCT_NAME + ".xcarchive"
EXPECT_OPTION_FILE_NAME = "ExportOptions.plist"

# 导出包配置文件
EXPORT_SETTING_FILE = EXPECT_OPTION_PATH + EXPECT_OPTION_FILE_NAME

#fir.im params 上传包参数，可在官网文档查看
Fir_token = ""
Fir_aPPId = ""

#输出构建包路径
print (BUILD_PATH)
#导出包全部路径
print (EXPORT_SETTING_FILE)

#邮件内容配置
newVersionMsg0 = "【发件人:张三\n"
email_title = "项目名称"
#安装包下载地址
downloadPath = ""
PRODUCT_DISPlayName = email_title + newVersionMsg0


#发件人账户
email_user=''
#1.登录qq邮箱后；2.选择设置-账户；3.开启服务：POP3/SMTP服务；4.获取email_password
#5、具体详细步骤:https://blog.csdn.net/dkq972958298/article/details/78432704
email_password = ''
#收件人邮箱
email_to_user_list = ["2442410527@qq.com",
                      "1158538647@qq.com"]

#打包
def buildWorkspace():
	archiveCmd = 'xcodebuild -archivePath %s -workspace %s.xcworkspace -sdk iphoneos -scheme %s archive' %(BUILD_PATH,PRODUCT_NAME,PRODUCT_NAME)
	process = subprocess.Popen(archiveCmd,shell=True)
	process.wait()

	archiveReturnCode = process.returncode 
	if archiveReturnCode != 0:
		print ("\n************archive faild ********************")
	else:
		print ("\n******************** archive success ********************")
		exportIpa()

#导出包
def exportIpa():
	exportCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s -allowProvisioningUpdates' %(BUILD_PATH,IPA_EXPORTPATH,EXPORT_SETTING_FILE)
	process = subprocess.Popen(exportCmd,shell=True)
	process.wait()

	archiveReturnCode = process.returncode
	if archiveReturnCode !=0:
		print ("\n******************** exportIpa faild ********************")
	else:
		print ("\n******************** exportIpa success ********************")
		cleanArchiveFile()

def cleanArchiveFile():
	cleanCmd = "rm -r ./build"
	process = subprocess.Popen(cleanCmd, shell=True)
	process.wait()

	archiveReturnCode = process.returncode
	if archiveReturnCode != 0:
		print ("\n******************** clean faild ********************")
	else:
		print ("\n******************** clean success ********************")
#            AliasIpaToFirI()

#检验包
def AliasIpaToFirI():
    aliasCmd = 'fir p %s/%s.ipa' %(IPA_EXPORTPATH,PRODUCT_NAME)
    process = subprocess.Popen(aliasCmd, shell=True)
    process.wait()

    aliasReturnCode = process.returncode
    if aliasReturnCode != 0:
        print ("alias faild")
    else:
        print ("alias success")
        loginToFirIm()

# login fir account
def loginToFirIm():
    loginCmd = 'fir login -T %s' %(Fir_token)
    process = subprocess.Popen(loginCmd, shell=True)
    process.wait()

    loginReturnCode = process.returncode
    if loginReturnCode != 0:
        print ("login faild")
    else:
        print ("login success")
        publishToFirIm()

# publish
def publishToFirIm():
    publishCmd = 'fir publish %s/%s.ipa' %(IPA_EXPORTPATH,PRODUCT_NAME)
    process = subprocess.Popen(publishCmd, shell=True)
    process.wait()

    publishReturnCode = process.returncode
    if publishReturnCode != 0:
        print ("publish faild")
    else:
        print ("publish success")

        des = input("Please input new version description:")
        send_qq_email(PRODUCT_DISPlayName,des)

# send email
def send_qq_email(title,content):
    try:
        newVersionMsg1 = email_title + "本("
        newVersionMsg2 = ")已更新，请前往 \n\n"
        newVersionMsg = newVersionMsg1 + APP_VERSION + newVersionMsg2
        content = newVersionMsg + downloadPath + " 下载,密码:'aaa',更新内容:\n" + content

        msg = MIMEText(str(content))
        msg["Subject"] = title
        msg["From"] = email_user
        msg["To"] = ";".join(email_to_user_list)

        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(email_user, email_password)
        s.sendmail(email_user, email_to_user_list, msg.as_string())
        s.quit()
        print ("\n*************** email send successfully! *********************\n")
        return True
    except smtplib.SMTPException:
        print ("\n*************** email send failure! *********************\n")
        return False

def main():

    buildWorkspace()
    AliasIpaToFirI()
#    des = input("Please input new version description:")
#    send_qq_email(PRODUCT_DISPlayName,des)

if __name__ == '__main__':
	main()
