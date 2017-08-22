<?php
require '../wechat-php-sdk/autoload.php';

use Gaoming13\WechatPhpSdk\Wechat;

$wechat = new Wechat(array( 
    'appId'         =>  'abcdefg',
    'token'         =>  'abcdefgabcdefg'
    'encodingAESKey' => 'abcdefgabcdefgabcdefg'
));

$PRINTER_URL = 'https://192.168.102.130:20000/print';
$PRINTER_USERS = array('YOUR_ID-OR_DELETE_THIS_CHECK',);
$PRINTER_KEY = "AABBCCDD";

function print_image($username, $url){
    global $PRINTER_USERS, $PRINTER_KEY, $PRINTER_URL;
    if (in_array($username, $PRINTER_USERS)){
        $data = array("Auth" => $PRINTER_KEY, "IMG_URL" => $url, "USER" => $username);
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $PRINTER_URL);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST,  0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
        $output = curl_exec($ch);
        curl_close($ch);
        return $output;
    }
    else{
        return "You are not authorized to use this printer. \nPlease contact ihciah@gmail.com.";
    }
}

$msg = $wechat->serve();
if ($msg->MsgType == 'text' && $msg->Content == 'id' || $msg->Content == 'whoami') {
    $wechat->reply(strval($msg->FromUserName));
}
else if ($msg->MsgType == 'text' && $msg->Content == 'time') {
    $wechat->reply(strval($msg->CreateTime));
}
else if ($msg->MsgType == 'image'){
    $wechat->reply(strval(print_image(strval($msg->FromUserName), strval($msg->PicUrl))));
}
else {
    $wechat->reply(strval($msg->Content));
}
