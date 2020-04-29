# Grafana
## **1) Cấu hình mail SMTP**
### **Mời user xem/edit Dashboard**
```
# vi /etc/grafana/grafana.ini
```
<img src=https://i.imgur.com/yDGcngF.png>

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
