#! /bin/sh
#按照提示来输入配置参数
setup()
{
    echo "输入你的服务器的IP地址："
    read server
    echo "输入想设定的服务器接口（推荐大于2000的四位数或五位数如9400）："
    read server_port
    echo "输入你要设置的密码："
    read passwd

    echo
    echo
    echo "配置如下："
    echo "ip          :${server}"
    echo "password    :${passwd}"
    echo "port        :${server_port}"
    echo "metho       :aes-256-cfb"
    echo
    echo
}
setup
while :
do
    echo "确定配置信息吗[Y/n]\c"
    read sure
    if [ ${sure:=y} = "n" ] || [ ${sure:=y} = "N" ]; then
        setup
    else
        break
    fi
done

#生成json文件
config="/etc/shadowsocks.json"
if [ -f "${config}" ]; then
    `rm $config`
fi
`touch $config`
`echo { >> $config`
`echo "\"server\":\"${server}\"," >> $config`
`echo "\"server_port\":${server_port}," >> $config`
`echo "\"local_port\":1080," >> $config`
`echo "\"password\":\"${passwd}\"," >> $config`
`echo "\"timeout\":300," >> $config`
`echo "\"method\":\"aes-256-cfb\"" >> $config`
`echo } >> $config`

echo `ssserver -c "${config}" -d start`
#开启BBR拥塞算法，提高速度
sysctl net.core.default_qdisc=fq
sysctl net.ipv4.tcp_congestion_control=bbr
lsmod | grep bbr