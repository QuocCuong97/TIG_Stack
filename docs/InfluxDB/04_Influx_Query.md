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
- Sử dụng với **TIMESTAMP** :

