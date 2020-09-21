# Cài đặt Diamond
## **1) Giới thiệu**
- **Diamond** là một python daemon thu thập metrics và đẩy chúng lên **Graphite**, hoặc các nguồn khác. Nó có khả năng thu thập metric của CPU, memory, network, I/O, load, disk. Thêm vào đó, **diamond** cung cấp API cho phép tự tạp các collector riêng để collect metric từ nhiều nguồn khác nhau .
- Documentation : https://diamond.readthedocs.io/en/latest/
- GitHub : https://github.com/python-diamond/diamond
## **2) Cài đặt**
### **2.1) Cài đặt trên CentOS 7**
- **B1 :** Update các package đã có :
    ```
    # yum update -y
    # yum upgrade -y
    ```
- **B2 :** Cài đặt các packet cần thiết :
    ```
    # yum install make rpm-build python-devel mysql-devel gcc -y
    ```
- **B3 :** Cài đặt pip và các thư viện cần thiết :
    ```
    # yum install -y python-pip
    ```
- **B4 :** Clone source code :
    ```
    # git clone git@git.paas.vn:CloudOps/diamond.git
    ```
- **B5 :** Cài đặt các thư viện cần thiết :
    ```
    # pip install -r requirements.txt
    # pip install xml-python libvirt-python
    ```
- **B5 :** Build file cài đặt :
    ```
    # cd diamond/
    # make buildrpm
    ```
- **B6 :** Cài đặt file vừa build :
    ```
    # yum localinstall -y --nogpgcheck dist/diamond-4.0.398-0.noarch.rpm
    ```
- **B7 :** Copy file cấu hình diamond từ file mẫu :
    ```
    # cp /etc/diamond/diamond.conf.example /etc/diamond/diamond.conf
    ```
- **B8 :** Khởi động dịch vụ `diamond` :
    ```
    # systemctl enable diamond
    # systemctl start diamond
    ```