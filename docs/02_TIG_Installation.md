# Cài đặt TIG Stack
## **1) Cài đặt trên CentOS 7**
## **2) Cài đặt trên Ubuntu Server 18.04**
### **2.1) Cài đặt InfluxDB**
- **B1 :** Thêm Influxdata key :
    ```
    # sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
    ```
- **B2 :** Thêm repositorty Influxdata và update lại các thay đổi :
    ```
    # source /etc/lsb-release
    # echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
    # sudo apt update -y
    ```
- **B3 :** Cài đặt gói `influxdb` :
    ```
    # apt install influxdb -y
    ```
- **B4 :** Khởi động dịch vụ và cấu hình khởi động cùng hệ thống :
    ```
    # systemctl start influxdb
    # systemctl enable influxdb
    ```
- **B5 :** Kiểm tra trạng thái dịch vụ :
    ```
    # systemctl status influxdb
    ```
    <img src=https://i.imgur.com/FrD2fkv.png>

- **B6 :** Kiểm tra port đang mở :
    ```
    # netstat -plntu
    ```
    <img src=https://i.imgur.com/JIDrjJW.png>

- **B7 :** Kiểm tra version hiện tại của **Influx** :
    ```
    # influx -version
    ```
    <img src=https://i.imgur.com/gV6N7ZW.png>

- **B8 :** Để lưu trữ dữ liệu cho **Telegraf agents**, ta sẽ setup trước database và user trên **Influxdb** :
    ```
    # influx
    ```
    <img src=https://i.imgur.com/pELvFb2.png>

    > Lúc này ta đang kết nối đến **Influx server** mặc định trên port `8086`.
- **B9 :** Tạo database và user cho **Telegraf** :
    ```
    > create database telegraf
    > create user telegraf with password 'P@ssw0rd'
    ```
- **B10 :** Kiểm tra lại database và user vừa tạo :
    ```
    > show databases
    > show users
    ```
    <img src=https://i.imgur.com/hkNP1DU.png>

    > Gõ `exit` để thoát .
### **2.2) Cài đặt Telegraf Agent**
- **B1 :** Cài đặt package `telegraf` :
    ```
    # apt install telegraf -y
    ```
- **B2 :** Khởi động dịch vụ và cấu hình khởi động cùng hệ thống :
    ```
    