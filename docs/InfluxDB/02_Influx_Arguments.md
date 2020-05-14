# Influx Arguments
- Một vài đối số có thể truyền vào khi bắt đầu lệnh `influx` . Sử dụng lệnh `influx --help` để hiển thị list các đối số :
    
    <img src=https://i.imgur.com/SFAv5mn.png>

### **Thực hiện command không cần vào InfluxCLI với `--execute`**
- **VD :**
    ```
    # influx -execute 'SHOW DATABASES'
    ```
    <img src=https://i.imgur.com/gWnQNxs.png>

### **Chỉ định định dạng dữ liệu truy vấn trả về với `-format`**
- **VD1 :** Truy vấn trả về kiểu dữ liệu `column` (mặc định, không cần khai báo)
    ```
    # influx
    hoặc
    # influx -format=column
    ```
    <img src=https://i.imgur.com/XBGCZjP.png>

- **VD2 :** Truy vấn trả về kiểu dữ liệu `csv` :
    ```
    # influx -format=csv
    ```
    <img src=https://i.imgur.com/Y9npOPO.png>

- **VD3 :** Truy vấn trả về kiểu dữ liệu `json` :
    ```
    # influx -format=json
    ```
    <img src=https://i.imgur.com/AEfodsq.png>

- **VD4 :** Truy vấn trả về kiểu dữ liệu `json` - dạng dễ nhìn hơn :
    ```
    # influx -format=json -pretty
    ```
    <img src=https://i.imgur.com/l2G404J.png>

### **Import dữ liệu vào database với `-import`**
- [Tham khảo thêm](https://docs.influxdata.com/influxdb/v1.8/tools/shell/#import-data-from-a-file-with-import)
