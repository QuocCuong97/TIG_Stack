# Tổng quan về TIG Stack
## **1) Monitoring System**
- **Monitoring System** là một hệ thống theo dõi, ghi lại các trạng thái, hoạt động của máy tính hay ứng dụng một cách liên tục .
- Lý do sử dụng **Monitoring System** :
    - Dựa vào kết quả của hệ thống monitoring chúng ta có thể điêù chỉnh việc sử dụng tài nguyên (cpu, ram, disk, ...) sao cho phù hợp
    - Ngăn chặn các sự cố có thể xảy ra, nếu có xảy ra chúng ta cũng có thể phát hiện sớm hơn
    - Giảm thiểu thời gian quản lý hệ thống .
- Đặc điểm của một hệ thống monitor :
    - Xử lí real time
    - Có hệ thống cảnh báo
    - Visualization
    - Có khả năng tạo reports
    - Có khả năng cài cắm các plugins
- Thông thường một hệ thống monitoring thường có 4 thành phần chính:
    - Collector: Được cài trên các máy agent (các máy muốn monitor), có nhiệm vụ collect metrics của host và gửi về database. Ví dụ: Cadvisor, Telegraf, Beat, ...
    - Database: Lưu trữ các metrics mà colletor thu thập được, thường thì chúng ta sẽ sử dụng các time series database. Ví dụ ElasticSearch, InfluxDB, Prometheus, Graphite (Whisper)
    - Visualizer: Có nhiệm vụ trực quan hóa các metrics thu thập được qua các biểu đồ, bảng, .... Ví dụ: Kibana, Grafana, Chronograf
    - Alerter: Gửi thống báo đến cho sysadmin khi có sự cố xảy ra

<img src=https://i.imgur.com/3Spb4Rx.png>

- Có rất nhiều stack cho **monitoring system** phổ biến như :
    - Logstash - Elasticsearch - Kibana
    - Prometheus - Node Exporter - Grafana
    - Telegraf - InfluxDB - Grafana
## **2) TIG Stack**
- Bao gồm **Telegraf** - **InfluxDB** - **Grafana**

    <img src=https://i.imgur.com/2YHnSbi.png>

- **Telegraf** và **Influxdb** đều là sản phẩm của **InfluxData**, cả hai đều mà mã nguồn mở và được viết bởi **Go**. Mặc dù **InfluxData** cung cấp một stack hoàn chỉnh để monitor với **Chronograf** để visualize và **Kapacitor** để alerting (**TICK stack**) nhưng chúng ta có thể sử dụng Grafana để thay thế cho cả **Chronograf** lẫn **Kapacitor** .
### **2.1) Telegraf**
- Trang chủ: https://www.influxdata.com/time-series-platform/telegraf/
- **Telegraf** là một agent để collecting và reporting metrics và data được viết bởi **Go**.
- Nó có thể tích hợp để collect nhiều loại nguồn dữ liệu khác nhau của metrics, events, và logs trực tiếp từ containers và system mà nó chạy trên đó. Nó cũng có thể pull metrics từ các third-party APIs, Kafka. Nó cũng có nhiều output plugin để gửi metrics thu thập được tới nhiều dạng datastores, services, message queues khác nhau như **InfluxDB**, **Graphite**, **OpenTSDB**, **Datadog**, **Librato**, **Kafka**,...
### **2.2) InfluxDB**
- Trang chủ: https://www.influxdata.com/products/influxdb/
- **InfluxDB** là một **Time Series Database** (là database được tối ưu hóa để xử lý dữ liệu chuỗi thời gian, các dãy số được lập chỉ mục theo thời gian. )
- **InfluxDB** được sử dụng để lưu các dữ liệu cho các trường hợp liên quan đến một lượng lớn time-stamped data, bao gồm DevOps monitoring, log data, application metrics, IoT sensor data, và real-time analytics. Nó có thể tự động xóa các dữ liệu cũ, không cần thiết và cung cấp một ngôn ngữ giống **SQL** để tương tác với dữ liệu.
- Data trong **InfluxDB** được tổ chức dưới dạng time series. Time series có thể có một hoặc nhiều points, mỗi point là một mẫu rời rạc các số liệu. Point gồm:
    - Time (timestamp)
    - Một measurement (ví dụ "`cpu_load`")
    - Ít nhất một key-value field (giá trị đo được, ví dụ "`value=0.64`", hoặc "`temperature=21.2`")
    - Không hoặc nhiều key-value tags chứa metadata của value (ví dụ “`host=server01`”, “`region=EMEA`”, “`dc=Frankfurt`”)
- Chúng ta có thể xem measurement như là table trong sql có primary index luôn là time. tags và field là columns của table, tags được index còn field thì không. Điểm khác biệt ở đây là **InfluxDB** có thể có hàng triệu measurements, chúng ta không cần định nghĩa schemas trước và giá trị null không được lưu trữ.
- **InfluxDB** có thể xử lý được hàng trăm nghìn dữ liệu trong 1 giây. Cách lưu trữ dữ liệu giúp nó làm được điều này.
- **InfluxDB** cung cấp 2 tính năng là **Continuous Queries (CQ)** và **Retention Policies (RP)**. Chúng sẽ tự động xử lí downsampling data và expiring old data.
- **Continuous Query (CQ)** là một **InfluxQL** query cái mà sẽ chạy tự động và theo định kỳ trong database. **CQs** yêu cầu một function trong mệnh đề `SELECT` và phải bao gồm mệnh đề GROUP BY time() - có thể hiểu là thằng này sẽ chạy trước các câu truy vấn của mình.
- **Retention Policy (RP)** là một phần của **InfluxDB**’s data structure, biểu thị thời gian mà InfluxDB lưu giữu data. InfluxDB sẽ so sánh giữa thời gian của host với thời gian của dữ liệu và xóa bỏ các dữ liệu có thời gian cũ hơn **RP**’s DURATION (do chúng ta cấu hình). Một single database có thể có một số **RPs** và **RPs** là duy nhất cho mỗi database.
### **2.3) Grafana**
- Trang chủ: https://grafana.com/grafana/
- Là một mã nguồn mở cho phép chúng ta query, visualize, alert các metrics thu thập được.
- Các tính năng của Grafana:
    - Visualize: table, chart, ...
    - Alert: alert to email, slack, ...
    - Unify: Hỗ trợ nhiều loại database như InfluxDB, ElasticSearch, Graphite, ...
    - Open: mã nguồn mở, có thể chạy trên nhiều hệ điều hành, có office Docker image
    - Extend: Cung cấp nhiều plugin, nhiều dashboard template
    - Collaborate: Hỗ trợ teamwork