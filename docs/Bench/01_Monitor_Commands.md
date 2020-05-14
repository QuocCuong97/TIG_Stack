# Các lệnh giám sát trong Linux
## **1) `ps`**
- Dữ liệu hiển thị đầy đủ khi thực hiện lệnh :
    ```
    # ps -aux
    ```
    <img src=https://i.imgur.com/zWPSRtR.png>

- Hiển thị các cột theo dạng custom :
    ```
    # ps -eo pid,ppid,%cpu,%mem
    ```
    <img src=https://i.imgur.com/Al9IaEA.png>

- Sắp xếp các tiến trình theo cột :
    ```
    # ps -eo pid,pidd,cmd,%cpu,%mem --sort=%mem (từ thấp đến cao)
    ```

    <img src=https://i.imgur.com/ljj2Msy.png>

    ```
    # ps -eo pid,pidd,cmd,%cpu,%mem --sort=-%mem (từ cao xuống thấp)
    ```

    <img src=https://i.imgur.com/WHYMmmN.png>

## **2) `watch`**
- Sử dụng để theo dõi hoạt động của process theo realtime
- Theo dõi dữ liệu cập nhật `1s` 1 lần .
    ```
    # watch -n 1 'ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 3'
    ```
    <img src=https://i.imgur.com/8WELuTx.png>

