# Cài đặt TIG Stack
## **1) Cài đặt trên CentOS 7**
## **2) Cài đặt trên Ubuntu Server 18.04**
### **2.1) Cài đặt InfluxDB**
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

- **B9 :** Để lưu trữ dữ liệu cho **Telegraf agents**, ta sẽ setup trước database và user trên **Influxdb** :
    ```
    # influx
    ```
    <img src=https://i.imgur.com/pELvFb2.png>

    > Lúc này ta đang kết nối đến **Influx server** mặc định trên port `8086`.
- **B10 :** Tạo database và user cho **Telegraf** :
    ```
    > create database telegraf
    > create user telegraf with password 'P@ssw0rd'
    ```
- **B11 :** Kiểm tra lại database và user vừa tạo :
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
    # systemctl start telegraf
    # systemctl enable telegraf
    ```
- **B3 :** Kiểm tra trạng thái dịch vụ :
    ```
    # systemctl status telegraf
    ```
    <img src=https://i.imgur.com/wVajxS3.png>

- **B4 :** Kiểm tra version hiện tại của **Telegraf** :
    ```
    # telegraf --version
    ```
    <img src=https://i.imgur.com/SUtROr2.png>

- **B5 :** Backup file cấu hình mặc định của **Telegraf** :
    ```
    # cd /etc/telegraf/
    # cp telegraf.conf telegraf.conf.bak
    ```
- **B6 :** Chỉnh sửa file cấu hình `telegraf.conf` :
    ```
    # vi telegraf.conf
    ```
    - Chỉnh sửa một số dòng sau :

        <img src=https://i.imgur.com/nunzrLb.png>

        <img src=https://i.imgur.com/epGCpHw.png>

        <img src=https://i.imgur.com/ZKDikuI.png>

        <img src=https://i.imgur.com/MBBHdVm.png>

        <img src=https://i.imgur.com/TwfUmL6.png>

        <img src=https://i.imgur.com/V4HuoFv.png>

        <img src=https://i.imgur.com/i0e7G1N.png>

        <img src=https://i.imgur.com/kU3Gz7k.png>

        <img src=https://i.imgur.com/KYpLIvf.png>

        <img src=https://i.imgur.com/lFu5b6h.png>

        <img src=https://i.imgur.com/xPgqF0Z.png>

        <img src=https://i.imgur.com/RHTPfvM.png>

        <img src=https://i.imgur.com/hSru96N.png>

        <img src=https://i.imgur.com/Al0V65v.png>

- **B7 :** Khởi động lại dịch vụ :
    ```
    # systemctl restart telegraf
    ```
- **B8 :** Kiểm tra trạng thái của các input :
    - Kiểm tra `cpu` input :
        ```
        # telegraf -test -config /etc/telegraf/telegraf.conf --input-filter cpu
        ```
        <img src=https://i.imgur.com/vcOG1uv.png>
    - Kiểm tra `net` input :
        ```
        # telegraf -test -config /etc/telegraf/telegraf.conf --input-filter net
        ```
        <img src=https://i.imgur.com/XLK7EoY.png>
    - Kiểm tra `mem` input :
        ```
        # telegraf -test -config /etc/telegraf/telegraf.conf --input-filter mem
        ```
        <img src=https://i.imgur.com/FVaqJ8a.png>

### **2.3) Cài đặt Grafana**
- **B1 :** Thêm Grafana key và repository :
    ```
    # apt-get install -y adduser libfontconfig1
    # wget https://dl.grafana.com/oss/release/grafana_6.7.3_amd64.deb
    ```
- **B2 :** Cài đặt package **Grafana** :
    ```
    # dpkg -i grafana_6.7.3_amd64.deb
    ```
- **B3 :** Khởi động dịch vụ và cấu hình khởi động cùng hệ thống :
    ```
    # systemctl start grafana-server
    # systemctl enable grafana-server
    ```
- **B4 :** Cho phép port `3000` đi qua **firewall** :
    ```
    # ufw allow 3000/tcp
    ```
- **B5 :** Kiểm tra trạng thái dịch vụ :
    ```
    # systemctl status grafana-server
    ```
    <img src=https://i.imgur.com/i8kago2.png>
- **B6 :** Kiểm tra port đang mở :
    ```
    # netstat -plntu
    ```
    <img src=https://i.imgur.com/bh47xiX.png>
- **B7 :** Kiểm tra version hiện tại của **Grafana** :
    ```
    # grafana-servef -v
    ```
    <img src=https://i.imgur.com/JVQcK27.png>

- **B8 :** Setup **Grafana**  - truy cập URL sau trên trình duyệt của client , đăng nhập với user mặc định `admin/admin` -> ***Login*** :
    ```
    http://<ip-grafana-server>:3000
    ```
    <img src=https://i.imgur.com/o1xixfN.png>

- **B9 :** **Grafana** sẽ yêu cầu đổi password mặc định ngay lần đăng nhập đầu tiên :

    <img src=https://i.imgur.com/zsxmH6w.png>

- **B10 :** Chọn ***Create a data source*** :

    <img src=https://i.imgur.com/JyeU7ci.png>

- **B11 :** Chọn ***InfluxDB*** để liên kết với **InfluxDB** vừa cài ở trên :

    <img src=https://i.imgur.com/uck4Cra.png>

- **B12 :** Điền các thông tin cần thiết để giám sát **Telegraf**, sau đó chọn ***Save & Test*** :

    <img src=https://i.imgur.com/zEgu85f.png>

    <img src=https://i.imgur.com/yDIRbfL.png>

- **B13 :** Liên kết thành công :

    <img src=https://i.imgur.com/pemRVbk.png>

- **B14 :** 

    <img src=https://i.imgur.com/nzntCte.png>

- **B15 :** 

    <img src=https://i.imgur.com/uUWoNJo.png>

- **B16 :**

    <img src=https://i.imgur.com/YZl8ysm.png>

- **B17 :**

    <img src=https://i.imgur.com/es1w3Ar.png>