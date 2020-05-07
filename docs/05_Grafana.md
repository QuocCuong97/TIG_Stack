# Grafana
## **1) Cấu hình mail SMTP**

```
# vi /etc/grafana/grafana.ini
```
- Truy cập các đường dẫn sau đối với tài khoản Google :
    - https://myaccount.google.com/lesssecureapps               Bật
    - https://accounts.google.com/b/0/DisplayUnlockCaptcha      Bật

<img src=https://i.imgur.com/CO1FwwC.png>

<img src=https://i.imgur.com/eVNazii.png>


## **2) Cài đặt thêm Plugins**
plugins sẽ được lưu trong `/var/lib/grafana/plugins`
### **2.1) Google Calendar**
```
grafana-cli plugins install mtanda-google-calendar-datasource
```
Chưa xong

### **2.2) Google Authen**
<img src=https://i.imgur.com/Ns4mKyl.png>

### **2.3) GitHub Authen**

<img src=https://i.imgur.com/pXGHVz8.png>

<img src=https://i.imgur.com/XASvb8K.png>

## **3) Cấu hình cảnh báo**



## **1) Cài đặt trên CentOS 7**
- **B1 :**
    ```
    vim /etc/yum.repos.d/grafana.repo
    ```
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
- **B2 :**
    ```
    # yum repolist
    ```
- **B3 :** 
    ```
    # yum install grafana -y
    ```
- **B4 :**
    ```
    # systemctl start grafana-server
    systemctl enable grafana-server
    ```
- **B5 :**
    ```
    firewall-cmd --zone=public --add-port=3000/tcp --permanent
    firewall-cmd --reload
    ```


## **Embed**
- **B1 :** Thay đổi trong file `grafana.ini`
    ```
    # vi /etc/grafana/grafana.ini
    ```
    - Chỉnh sửa các dòng sau :

        <img src=https://i.imgur.com/HzaZXNO.png>

        <img src=https://i.imgur.com/58e4mKO.png>

        <img src=https://i.imgur.com/bujp6sH.png width=89%>

        <img src=https://i.imgur.com/Oy2uNsg.png width=87%>

- **B2 :** Trên dashboard của **Grafana**, vào Panel muốn nhúng, chọn ***Edit*** :

    <div align=center><img src=https://i.imgur.com/GG4kkL6.png width=70%></div>

- **B3 :** Trong tab **Embed** , copy đoạn code thẻ `<iframe>` và paste vào trong code html của trang web nhúng :

    <div align=center><img src=https://i.imgur.com/eU6ejAj.png width=70%></div>

    - Lưu ý :
        - Xóa đoạn `&from=xxxxxxxxxxxxx&to=xxxxxxxxxxxxx` trong link để iframe hiển thị là real-time
        - Thay đổi `&refresh=xx` với `xx` là thời gian update cho panel
        - Thêm `&theme=light` nếu muốn đổi panel thành nền sáng
        - Thay đổi kích cỡ iframe qua thuộc tính `width` và `height`
- **B4 :** Kết quả :

    <img src=https://i.imgur.com/dLfFz8T.png>


## **Disable Grafana Preloader**
- Chỉnh sửa file 
    ```
    vi /usr/share/grafana/public/views/index.html
    ```
    - Comment lại đoạn sau :

        <img src=https://i.imgur.com/aX6O1Ll.png>

## **Edit template cảnh báo Email**
- Backup lại file template ban đầu :
    ```
    cd /usr/share/grafana/public/emails/
    cp alert_notification.html alert_notification.html.bak
    ```
- Chỉnh sửa template theo ý muốn :
    ```
    vi alert_notification.html
    ```