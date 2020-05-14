# InfluxDB
## **1) Giới thiệu**
## **2) Cài đặt**
### **2.1) Cài đặt trên CentOS 7**
- **B1 :** Tạo repo cho **InfluxDB** :
    ```
    # vi /etc/yum.repos.d/influxdb.repo
    ```
    - Thêm vào nội dung sau :
        ```
        [influxdb]
        name = InfluxDB Repository - RHEL $releasever
        baseurl = https://repos.influxdata.com/rhel/$releasever/$basearch/stable
        enabled = 1
        gpgcheck = 1
        gpgkey = https://repos.influxdata.com/influxdb.key
        ```
    - Cập nhật lại các repo :
        ```
        # yum repolist
        ```
- **B2 :** Cài đặt **InfluxDB** :
    ```
    # yum install influxdb -y
    ```
- **B3 :** Khởi động dịch vụ và cấu hình khởi động cùng hệ thống :
    ```
    # systemctl start influxdb
    # systemctl enable influxdb
    ```
- **B4 :** Cho phép các port `8066` và `8088` đi qua **FirewallD** :
    ```
    # firewall-cmd --permanent --add-port=8086/tcp
    # firewall-cmd --permanent --add-port=8088/tcp
    # firewall-cmd --reload
    ```
- **B5 :** Kiểm tra trạng thái dịch vụ :
    ```
    # systemctl status influxdb
    ```
    <img src=https://i.imgur.com/eJWGESm.png>

- **B8 :** Kiểm tra version hiện tại của **Influx** :
    ```
    # influx -version
    ```
    <img src=https://i.imgur.com/bkgEW72.png>

### **2.2) Cài đặt trên Ubuntu Server 18.04**
- **B1 :** Thêm Influxdata key :
    ```
    # wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
    ```
- **B2 :** Thêm repositorty Influxdata và update lại các thay đổi :
    ```
    # source /etc/lsb-release
    # echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | tee /etc/apt/sources.list.d/influxdb.list
    # apt update -y
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
- **B5 :** Cho phép port `8086` đi qua **firewall** :
    ```
    # ufw allow 8086/tcp
    ```
- **B6 :** Kiểm tra trạng thái dịch vụ :
    ```
    # systemctl status influxdb
    ```
    <img src=https://i.imgur.com/FrD2fkv.png>

- **B7 :** Kiểm tra port đang mở :
    ```
    # netstat -plntu
    ```
    <img src=https://i.imgur.com/JIDrjJW.png>

- **B8 :** Kiểm tra version hiện tại của **Influx** :
    ```
    # influx -version
    ```
    <img src=https://i.imgur.com/gV6N7ZW.png>

## **3) File cấu hình của InfluxDB**
## **4) Các cú pháp query**
- Vào trình quản lý command của **InfluxDB** :
    ```
    # influx
    ```
- Chọn database muốn thao tác :
    ```
    > use telegraf
    ```
### **4.1) Thao tác với measurements**
- Hiển thị danh sách các **MEASUREMENT** đã thu thập :
    ```
    > show measurements
    ```
    <img src=https://i.imgur.com/RAY924B.png>

- Hiển thị **TAG KEYS** của các **MEASUREMENT** :
    ```
    > show tag keys from cpu
    ```
    <img src=https://i.imgur.com/Vrsq3d8.png>

- Hiển thị các **TAG VALUES** của các **TAG KEYS** :
    ```
    > show tag values from cpu with key=host
    ```
    <img src=https://i.imgur.com/8lqxMv9.png>

- Hiển thị kiểu dữ liệu của các **MEASUREMENT** :
    ```
    > show field keys from cpu
    ```
    <img src=https://i.imgur.com/Z93a5cF.png>
### **4.2) Các query function**
#### **COUNT**
- Trả về số lượng của các non-null field values.
#### **MEAN**
- Trả về giá trị trung bình cho các giá trị trong một field duy nhất.
- 