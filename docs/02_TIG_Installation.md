# Cài đặt TIG Stack
## **1) Cài đặt trên CentOS 7**
### **1.1) Cài đặt InfluxDB**
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
    <img src=https://i.imgur.com/XwawmXW.png>

- **B6 :** Kiểm tra version hiện tại của **Influx** :
    ```
    # influx -version
    ```
    <img src=https://i.imgur.com/EQw4Zl7.png>

- **B7 :** Để lưu trữ dữ liệu cho **Telegraf agents**, ta sẽ setup trước database và user trên **Influxdb** :
    ```
    # influx
    ```
    <img src=https://i.imgur.com/LSIrjqQ.png>

    > Lúc này ta đang kết nối đến **Influx server** local mặc định trên port `8086`.
- **B8 :** Tạo database và user cho **Telegraf** :
    ```
    > create database telegraf
    > create user telegraf with password 'P@ssw0rd'
    ```
- **B9 :** Kiểm tra lại database và user vừa tạo :
    ```
    > show databases
    > show users
    ```
    <img src=https://i.imgur.com/KMIhI73.png>

    > Gõ `exit` để thoát .
### **1.2) Cài đặt Telegraf Agent**
- **B1 :** Cài đặt **Telegraf** :
    ```
    # yum install -y telegraf
    ```
- **B2 :** Khởi động dịch vụ và cấu hình khởi động cùng hệ thống :
    ```
    # systemctl start telegraf
    # systemctl enable telegraf
    ```
- **B3 :** Kiểm tra version hiện tại của **Telegraf** :
    ```
    # telegraf --version
    ```
    <img src=https://i.imgur.com/bGGoiCJ.png>

- **B4 :** Backup file cấu hình mặc định của **Telegraf** :
    ```
    # cd /etc/telegraf/
    # cp telegraf.conf telegraf.conf.bak
    ```
- **B5 :** Chỉnh sửa file cấu hình `telegraf.conf` :
    ```
    # vi telegraf.conf
    ```
    - Chỉnh sửa các dòng sau :
        ```
        ...
        hostname = "tig_server"             (dòng 94)
        ...
        [[outputs.influxdb]]
        ...
        urls = ["http://127.0.0.1:8086"]    (dòng 112)
        ...
        database = "telegraf"               (dòng 116)
        ...
        username = "telegraf"               (dòng 149)
        password = "P@ssw0rd"               (dòng 150)
        ...
        [[inputs.cpu]]                      (dòng 2614)
        ## Whether to report per-cpu stats or not
        percpu = true
        ## Whether to report total system cpu stats or not
        totalcpu = true
        ## If true, collect raw CPU time metrics
        collect_cpu_time = false
        ## If true, compute and report the sum of all non-idle CPU states
        report_active = false               (dòng 2622)
        ...
        [[inputs.disk]]                     (dòng 2626)
        ## By default stats will be gathered for all mount points.
        ## Set mount_points will restrict the stats to only the specified mount points.
        # mount_points = ["/"]
   
        ## Ignore mount points by filesystem type.
        ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]                 (dòng 2639)
        ...
        [[inputs.diskio]]
        ...
        [[inputs.kernel]]
        ...
        [[inputs.mem]]
        ...
        [[inputs.processes]]
        ...
        [[inputs.system]]
        ...
        [[inputs.net]]                      (dòng 4793)
        ...
        [[inputs.netstat]]                  (dòng 4835)
        ...
        ```
- **B6 :** Khởi động lại dịch vụ :
    ```
    # systemctl restart telegraf
    ```
### **1.3) Cài đặt Grafana**
- **B1 :** Tạo repo cho **Grafana** :
    ```
    # vim /etc/yum.repos.d/grafana.repo
    ```
    - Thêm vào nội dung sau :
        ```
        [grafana]
        name=grafana
        baseurl=https://packages.grafana.com/oss/rpm
        repo_gpgcheck=1
        enabled=1
        gpgcheck=1
        gpgkey=https://packages.grafana.com/gpg.key
        sslverify=1
        sslcacert=/etc/pki/tls/certs/ca-bundle.crt
        ```
    - Cập nhật lại các repo :
        ```
        # yum repolist
        ```
- **B2 :** Cài đặt `grafana` :
    ```
    # yum install grafana -y
    ```
- **B3 :** Khởi động dịch vụ và cấu hình khởi động cùng hệ thống :
    ```
    # systemctl start grafana-server
    # systemctl enable grafana-server
    ```
- **B4 :** Cho phép các port `3000` đi qua **FirewallD** :
    ```
    # firewall-cmd --zone=public --add-port=3000/tcp --permanent
    # firewall-cmd --reload
    ```
- **B5 :** Kiểm tra version hiện tại của **Grafana** :
    ```
    # grafana-server -v
    ```
    <img src=https://i.imgur.com/F12VhGz.png>

- **B6 :** Setup **Grafana** - truy cập URL sau trên trình duyệt của client , đăng nhập với user mặc định `admin/admin` -> ***Login*** :
    ```
    http://<ip-grafana-server>:3000
    ```
    <img src=https://i.imgur.com/mHkFKpz.png>

- **B7 :** **Grafana** sẽ yêu cầu đổi password mặc định ngay lần đăng nhập đầu tiên (hoặc có thể ***Skip*** để bỏ qua) :

    <img src=https://i.imgur.com/1MY4KAd.png>

- **B8 :** Trong tab **Configuration**, chọn **Data Sources** :

    <img src=https://i.imgur.com/2xEzSyO.png>

- **B9 :** Chọn ***Add data source*** :

    <img src=https://i.imgur.com/oMli4Sf.png>

- **B10 :** Chọn ***InfluxDB*** để liên kết với **InfluxDB** vừa cài ở trên :

    <img src=https://i.imgur.com/PVjYWsr.png>

- **B11 :** Điền các thông tin cần thiết để giám sát **Telegraf**, sau đó chọn ***Save & Test*** :

    <img src=https://i.imgur.com/gSRmhHu.png>

    <img src=https://i.imgur.com/KKfIX3J.png>

    - Liên kết database thành công sẽ có kết quả sau :

        <img src=https://i.imgur.com/n14ZZmS.png>

- **B12 :** Tại tab **Create**, chọn **Import** để thêm template dashboard đã có sẵn (được public) hoặc có thể tự vẽ dashboard :
    
    <img src=https://i.imgur.com/319HGGF.png>

    > Các template dashboard có thể xem thêm tại https://grafana.com/grafana/dashboards

- **B13 :** Thêm ID của dashboard template, chọn ***Load*** :

    <img src=https://i.imgur.com/YcbHrxS.png>

- **B14 :** Chọn data source, sau đó chọn ***Import*** :

    <img src=https://i.imgur.com/aKhT0Mj.png>

- Dashboard Grafana sau khi thêm thành công :

    <img src=https://i.imgur.com/Zx6CnQd.png>
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