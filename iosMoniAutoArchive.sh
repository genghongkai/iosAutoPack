#!/bin/sh

#命令操作步骤:
#我的工程名称是 BJPlace
#1、进入工程根目录下，也就是currentPath当前路径
## cd ~/app_bjs/new-ios-app/cfae-app-ios/BJPlace

#2、执行打包脚本，终端中执行命令如下：
## sh ~/desktop/iosMoniArchive/iosMoniAutoArchive.sh

#版本
app_version='2.1.0.22'

#shell脚本文件名
shellScripFileName='iosMoniAutoArchive.sh'
#exportOption.plist文件名
exportOptionFileName='ExportOptions.plist'

echo '---------build begain----------'

# 参数

currentPath=$(pwd)

expertOptionPath='/Users/genghongkai/Desktop/iosMoniArchive/'

echo "expertOptionPath : ${expertOptionPath}"

#复制文件
#cp -R ${expertOptionPath} ${currentPath}

# 项目workspace 名称
workspaceName='BJPlace'
# 打包target 名称
targetName='BJPlace'
# 打包类型，
releaseType='Release'
# 打包私钥密码
keychainPassword='123'
# 导出ipa路径
ipaPath="${expertOptionPath}${app_version}/"
# 打包文件路径
buildPath="${ipaPath}${targetName}.xcarchive"
# 导出配置
exportSettingFile="${expertOptionPath}${exportOptionFileName}"

#fir_token
fir_token=''
#fir_app_id
fir_app_id=''

echo "workspaceName : ${workspaceName}"
echo "targetName : ${targetName}"
echo "releaseType : ${releaseType}"
echo "keychainPassword : ${keychainPassword}"
echo "buildPath : ${buildPath}"
echo "ipaPath : ${ipaPath}"
echo "exportSettingFile : ${exportSettingFile}"


#-------------------------------------------------------------------

##创建文件路径(如果已存在，不创建)
echo '==== 创建ipa文件夹 ============================================'
mkdir ${ipaPath}

# clean 项目

echo '==== clean project ============================================'
echo ''
echo "exec cmd -----> xcodebuild clean -workspace ${workspaceName}.xcworkspace -scheme ${targetName}"
echo ''

xcodebuild clean -workspace ${workspaceName}.xcworkspace -scheme ${targetName}

# pod 更新

echo '==== pod updae ============================================'
echo ''
echo "exec cmd -----> pod install"
echo ''

pod install

echo '---------unlock keychain----------'
echo ''
echo "exec cmd -----> security unlock-keychain -p ${keychainPassword}"
echo ''


echo '---------begain build----------'
echo ''
echo "exec cmd -----> xcodebuild -archivePath ${buildPath} -workspace ${workspaceName}.xcworkspace -sdk iphoneos -scheme ${targetName} ${releaseType}"
echo ''
xcodebuild -archivePath ${buildPath} -workspace ${workspaceName}.xcworkspace -sdk iphoneos -scheme ${targetName} archive

echo '---------begain export----------'
echo ''
echo "exec cmd -----> xcodebuild -exportArchive -archivePath ${buildPath} -exportPath ${ipaPath} -exportOptionsPlist ${exportSettingFile} -allowProvisioningUpdates"
echo ''

xcodebuild -exportArchive -archivePath ${buildPath} -exportPath ${ipaPath} -exportOptionsPlist ${exportSettingFile} -allowProvisioningUpdates

echo '---------finish----------'

#--------------------------------------------------------------
#删除文件，exportOption.plist 和 iosMoniAutoArchive.sh
#rm ${shellScripFileName}
#rm ${exportOptionFileName}






#----------------------------------------------------------------
####开始上传，如果只需要打ipa包出来不需要上传，可以删除下面的代码

#检查文件是否存在
publish_ipa_path="${ipaPath}${targetName}.ipa"
echo "publish_ipa_path  : ${publish_ipa_path}"

if [ -f "${publish_ipa_path}" ] ; then
echo "\033[32;1m导出 ${targetName}.ipa 包成功 \033[0m"
open $export_path
else
echo "\033[31;1m导出 ${targetName}.ipa 包失败 \033[0m"
exit 1
fi

upload_token=$fir_token

echo '==== begin uploading ==========================================='
echo "正在上传到fir.im...."
fir p $ipaPath
changelog='更新安装包2.1.0.17'

fir login -T $upload_token       # fir.im token
echo "==== upload_token : ${upload_token}"
fir publish $ipaPath$targetName.ipa
echo '==== ${ipaPath}${targetName}.ipa ======================================'

curl http://api.fir.im/apps/latest/${fir_app_id}?api_token="74901ef9c447f4dcde583dd359f40ffc"
#curl http://api.fir.im/apps/5b72f175548b7a3b392b5f99?api_token="74901ef9c447f4dcde583dd359f40ffc"

echo '==== successfully uploading ==================================================='

