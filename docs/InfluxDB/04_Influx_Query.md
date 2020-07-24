# Influx Query
## **Mô hình Database**

<img src=https://i.imgur.com/EwzdP3e.png>

## **SHOW**
- Hiển thị các **DATABASE** hiện có :
    ```
    > show databases
    ```
    <img src=https://i.imgur.com/tJPUD0U.png>

- Hiển thị các **MEASUREMENT** đã thu thập :
    ```
    > use [database_name]
    > show measurements
    ```
    <img src=https://i.imgur.com/QvCf6Te.png>

- Hiển thị các **TAG_KEY** trong một **MEASUREMENT** :
    ```
    > show tag keys from [measurement_name]
    ```
    <img src=https://i.imgur.com/uCt9BQg.png>

- Hiển thị các **TAG_VALUE** trong một **TAG_KEY** :
    ```
    > show tag values from from [measurement_name] with key=[tag_key_name]
    ```
    <img src=https://i.imgur.com/QhiXnKf.png>

- Hiển thị các **FIELD_KEY** trong một **MEASUREMENT** :
    ```
    > show field keys from [measurement_name]
    ```
    <img src=https://i.imgur.com/FKfHY2b.png>

- Hiển thị các **USER** trong InfluxDB :
    ```
    > show users
    ```
    <img src=https://i.imgur.com/kD0pHJP.png>

## **SELECT**
- Sử dụng để truy vấn dữ liệu từ một **MEASUREMENT** riêng biệt hoặc nhiều **MEASUREMENT** .
- Cú pháp :
    ```
    select [field_key/tag_key] from [measurement_name]
    ```
    > Sử dụng `select *` nếu muốn hiển thị tất cả các giá trị 
- **VD1 :** Hiển thị tất cả các **tag_key** và **field_key** trong **measurement** `cpu` :
    ```
    > select * from cpu
    ```
    <img src=https://i.imgur.com/GKrJZET.png>

- **VD2 :** Hiển thị **field_key** `usage_system` và `usage_user` trong **measurement** `cpu` :
    ```
    > select usage_system, usage_user from cpu
    ```
    <img src=https://i.imgur.com/UtRvtht.png>

## **WHERE**
- Được sử dụng để thêm điều kiện cho câu truy vấn .
- Cú pháp chung :
    ```
    SELECT_clause FROM_clause WHERE <conditional_expression> [(AND|OR) <conditional_expression> [...]]
    ```
- Sử dụng với **FIELD_KEY** :
    ```
    WHERE field_key [operator] ['string' | boolean | float | integer]
    ```
    - Trong đó :
        - `operator`:
            - `=` : bằng
            - `<>` : không bằng
            - `!=` : không bằng
            - `>` : lớn hơn
            - `>=` : lớn hơn hoặc bằng
            - `<` : nhỏ hơn
            - `<=` : nhỏ hơn hoặc bằng
        - [Các biểu thức toán học](https://docs.influxdata.com/influxdb/v1.8/query_language/math_operators/)
        - [Regular Expression](https://docs.influxdata.com/influxdb/v1.8/query_language/explore-data/#regular-expressions)
- Sử dụng với **TAG KEY** :
    ```
    WHERE tag_key [operator] ['tag_value']
    ```
    - Trong đó : 
        - `operator` :
            - `=` : bằng
            - `<>` : không bằng
            - `!=` : không bằng
        - [Regular Expression](https://docs.influxdata.com/influxdb/v1.8/query_language/explore-data/#regular-expressions)
    - **VD :**
        ```
        > select * from "cpu" WHERE "host" = 'centos7-03'
        ```
- Sử dụng với **TIMESTAMP** :

## **GROUP BY**
### **GROUP BY với tags**
- Truy vấn nhóm **GROUP BY** sử dụng 1 hoặc 1 bộ **tag** để lọc kết quả .
- Cú pháp :
    ```
    SELECT_clause FROM_clause [WHERE_clause] GROUP BY [* | <tag_key>[,<tag_key]]
    ```
> Nếu trong truy vấn có **WHERE** thì **GROUP BY** phải đứng sau **WHERE** .
- **VD1 :** GROUP BY 1 tag :
    ```
    select last(usage_system) from cpu group by host
    ```
    <img src=https://i.imgur.com/ywZUxad.png>

- **VD2 :** GROUP BY nhiều tag :
    ```
    select last(usage_system) from cpu group by host, cpu
    ```
    <img src=https://i.imgur.com/nzvgugc.png>

- **VD3 :** GROUP BY tất cả các tag :
    ```
    select last(usage_system) from cpu group by *
    ```
### **GROUP BY với time()**
- Cú pháp :
    ```
    SELECT <function>(<field_key>) FROM_clause WHERE <time_range> GROUP BY time(<time_interval>),[tag_key] [fill(<fill_option>)]
    ```
    - Trong đó :
        - `time(<time_interval>)` là khoảng thời gian xác định cách các truy vấn nhóm GROUP BY truy vấn kết quả theo thời gian. VD với truy vấn `time interval() = 5m`, kết quả sẽ được nhóm thành các nhóm thời gian `5 phút` trong phạm vi thời gian được chỉ định trong mệnh đề `WHERE` .
        - `fill(<fill_option>)` là tham số tùy chọn . Nó sẽ thay đổi giá trị báo cáo trong khoảng thời gian không có dữ liệu .
> Truy vấn **GROUP BY time()** yêu cầu 1 mệnh đề `SELECT` và một mệnh đề `WHERE` :
- **VD1 :** 
    ```
    SELECT cpu,host,usage_system,usage_user FROM cpu WHERE time >= '2020-05-18T00:00:00Z' AND time <= '2020-05-18T08:30:00Z'
    ```
    <img src=https://i.imgur.com/qshyvZg.png>

    - Nhóm các kết quả truy vấn theo khoảng thời gian `1 phút` :
    ```
    SELECT count("usage_user") FROM "cpu" WHERE time >= '2020-05-18T00:00:00Z' AND time <= '2020-05-18T08:30:00Z' GROUP BY time(1m)
    ```

