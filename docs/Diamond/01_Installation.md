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
    # pip install xml-python libvirt-python
    ```
- **B4 :** Clone source code :
    ```
    # git clone git@git.paas.vn:CloudOps/diamond.git
    ```
- **B5 :** Cài đặt các thư viện cần thiết :
    ```
    # cd diamond/
    # pip install -r requirements.txt
    ```
- **B5 :** Build file cài đặt :
    ```
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
> Chú ý :
- Khi sử dụng **LibvirtKVMCollector**, khi gặp lỗi không đẩy được metric vào handler, thường là do lỗi conflict version `psutil`
- Để xử lý, thực hiện các bước sau :
    ```
    # rpm -qa | grep psutil
    python2-psutil-5.6.7-1.el7.x86_64
    # rpm -e python2-psutil-5.6.7-1.el7.x86_64 --nodeps
    # pip uninstall psutil
    # pip install psutil==5.0.1
    # yum install MySQL-python -y
    ```