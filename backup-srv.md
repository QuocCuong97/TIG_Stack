# Hướng dẫn deploy Backup Service môi trường Staging
### **Mô hình**
<img src=https://i.imgur.com/p7zZwK6.png>

### **Cài đặt chuẩn bị môi trường (cài đặt trên cả 5 node)**
- Bước 1: Update các package:
    ```
    yum update -y && yum upgrade -y
    ```
- Bước 2: Cài đặt các package cần thieste:
    ```
    yum install python3 wget git byobu -y
    ```
### **Cài đặt PostgreSQL (theo docs riêng)**
- Cài đặt PosgreSQL và các extension cần thiết. Tham khảo tại đây()
- Truy cập postgre shell:
    ```
    sudo -u postgres psql
    ```
- Set password cho user postgres:
    ```
    postgres=# \password postgres
    ```
- Kiểm tra các database đang có :
    ```
    postgres=# \l
    ```
- Sửa bind IP trong file cấu hình `/var/lib/pgsql/12/data/pg_hba.conf` thành :
    ```
    # IPv4 local connections:
    host    all             all             0.0.0.0/0               md5
    ```
- Sửa listen IP trong file cấu hình `/var/lib/pgsql/12/data/postgresql.conf` thành :
    ```
    # - Connection Settings -
    listen_addresses = '*'
    ```
    - Khởi động lại dịch vụ :
        ```
        systemctl restart postgresql-12
        ```
### **Cài đặt VerneMQ**
- Download package rpm :
    ```
    wget https://github.com/vernemq/vernemq/releases/download/1.11.0/vernemq-1.11.0.centos7.x86_64.rpm
    ```
- Cài đặt package :
    ```
    rpm -Uvh vernemq-1.11.0.centos7.x86_64.rpm
    ```
- Chấp nhận điều khoản dịch vụ trong file `/etc/vernemq/vernemq.conf` :
    ```
    accept_eula = yes
    ```
- Kích hoạt dịch vụ :
    ```
    systemctl start vernemq
    ```
- Chỉnh sửa listener IP trong file config :
    ```
    ...
    listener.tcp.default = 0.0.0.0:1883
    ...
    listener.http.default = 0.0.0.0:8888
    ...
    plugins.vmq_webhooks = on
    ...
    vmq_webhooks.webhook1.hook = auth_on_register
    vmq_webhooks.webhook2.hook = auth_on_publish
    vmq_webhooks.webhook3.hook = auth_on_subscribe
    vmq_webhooks.webhook4.hook = on_subscribe
    vmq_webhooks.webhook1.endpoint = http://10.5.69.110:5000/vernemq-webhooks
    vmq_webhooks.webhook2.endpoint = http://10.5.69.110:5000/vernemq-webhooks
    vmq_webhooks.webhook3.endpoint = http://10.5.69.110:5000/vernemq-webhooks
    vmq_webhooks.webhook4.endpoint = http://10.5.69.110:5000/vernemq-webhooks
    ...
    ```
- Khởi động lại dịch vụ :
    ```
    systemctl restart vernemq
    ```
- Lấy HTTP API Key :
    ```
    vmq-admin api-key create
    ```
### **Cài đặt Redis**
- Cài đặt Docker
- Chạy docker image :
    ```
    docker run -d -p 6379:6379 redis
    ```
### **Cài đặt Endeavour**
- Cài đặt Docker
- Clone Repo :
    ```
    git clone git@git.paas.vn:backup-service/endeavour.git
    cd endeavour
    git checkout develop
    ```
- Cài đặt `virtualenv` :
    ```
    pip3 install virtualenv
    virtualenv -p /usr/bin/python3 env
    source env/bin/activate
    ```
- Cài đặt các gói trong file `requirements.txt` :
    ```
    pip install -r requirements.txt
    ```
- Chỉnh sửa các thông tin trong file `config.py` :
    ```py
    SQLALCHEMY_DATABASE_URI = _get_env_or_default('DATABASE_URL',
                                                  'postgresql+psycopg2://postgres:vccloud123@10.5.69.113:5432/postgres')
    ....
    # Session
    SECRET_KEY = _get_env_or_default('SECRET_KEY', '386ee73b-73b0-4ff1-9a64-6eff4e3fe03b')

    # OPS
    OS_AUTH_URL = _get_env_or_default('OS_AUTH_URL', 'http://172.19.242.10:5000/v3')
    OS_USERNAME = _get_env_or_default('OS_USERNAME', 'admin')
    OS_PASSWORD = _get_env_or_default('OS_PASSWORD', 'V2VsY29tZTEyMw')
    OS_PROJECT_NAME = _get_env_or_default('OS_PROJECT_NAME', 'admin')
    OS_USER_DOMAIN_NAME = _get_env_or_default('OS_USER_DOMAIN_NAME', 'Default')
    OS_PROJECT_DOMAIN_NAME = _get_env_or_default('OS_PROJECT_DOMAIN_NAME', 'Default')
    OS_REGION_NAME = _get_env_or_default('OS_REGION_NAME', 'HaNoi')

    # Redis
    REDIS_HOST = _get_env_or_default('REDIS_HOST', '10.5.69.112')
    REDIS_PORT = _get_env_or_default('REDIS_PORT', 6379)

    # VMQ
    VMQ_HTTP_URL = _get_env_or_default('VMQ_URL_HTTP', 'http://10.5.69.114:8888/api/v1/session/show')
    VMQ_HTTP_API_KEY = 'HI9LAYzuWRSkxxIY2wFyMHuRMDHyRwDy'
    VMQ_HOST = _get_env_or_default('VMQ_HOST', '10.5.69.114')
    ...
    BROKER_URL = _get_env_or_default('BROKER_URL', 'mqtt://123.31.11.223:1883')    # IP Pub VMQ
    API_URL = _get_env_or_default('API_URL', 'https://backup-api.dev.bizflycloud.vn')
    ...
    RGW_ACCESS_KEY = _get_env_or_default(
        "RGW_ACCESS_KEY", '7M1HCLRCTKV46IPLA3U7')
    RGW_SECRET_KEY = _get_env_or_default(
        "RGW_SECRET_KEY", 'WPYle2ubh5vvuI9FMmQoHvLFJ9DCrGUzWeJjSlk2')
    RGW_REGION = _get_env_or_default("RGW_REGION", 'default')
    RGW_ENDPOINT = _get_env_or_default("RGW_ENDPOINT", 'http://10.3.52.157')
    ```
- Cài đặt Docker Compose :
    ```
    pip install docker-compose
    ```
- Build image `backup-api` :
    ```
    docker build -t backup-api .
    ```
- Trong file `docker-compose.yaml`, sửa cấu hình service `cloud-backup-api`:
    ```
    ...
    cloud-backup-api:
        image: backup-api
        container_name: cloud-backup-api
        restart: always
        ports:
        - "5000:5000"
    ...
- Khởi chạy các worker :
    ```
    docker-compose up -d cloud-backup-api
    docker-compose up -d cloud-backup-check_activate_machine
    docker-compose up -d cloud-backup-update_state_action
    ```
- Trong thư mục `endeavour`, migrate database :
    ```
    flask db stamp head
    flask db migrate
    flask db upgrade
    ```
### **Cài đặt HAProxy**
- Cài đặt NGINX
- Chỉnh sửa file config, thêm block sau vào block `http` :
    ```sh
    server {
        listen       80;
        server_name  backup-api.dev.bizflycloud.vn;                           # IP Pub
        #root         /usr/share/nginx/html;
        client_max_body_size 0;
        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
                proxy_pass      http://10.5.69.110:5000;     # Endpoint API
        }
        location ~ /endeavour-[A-Za-z0-9/._-]*$ {
                internal;
                proxy_set_header Authorization "";
                proxy_pass      https://ss-hn-1.vccloud.vn;         # RadosGW Endpoint
        }
    }
    ```
    - Khởi động lại service :
        ```
        systemctl restart nginx
        ```