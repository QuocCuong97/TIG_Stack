# Lệnh `sysbench`
## **1) Cài đặt**
### **1.1) Cài đặt trên Ubuntu/Debian**
- **B1 :** Update các package sẵn có :
    ```
    # apt update -y
    ```
- **B2 :** Cài đặt `sysbench` :
    ```
    # apt-get install sysbench -y
    ```
### **1.2) Cài đặt trên CentOS/RHEL**
- **B1 :** Cài đặt `epel-release` :
    ```
    # rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY*
    # yum -y install epel-release
    ```
- **B2 :** Update các package sẵn có :
    ```
    # yum update -y
    ```
- **B3 :** Cài đặt `sysbench` :
    ```
    # yum install sysbench -y
    ```
## **2) Sử dụng `sysbench` để benchmark hệ thống**
### **2.1) Benchmark CPU**
- Sử dụng lệnh :
    ```
    # sysbench --test=cpu --cpu-max-prime=20000 run
    ```
    => Output :
    ```
    WARNING: the --test option is deprecated. You can pass a script name or path on the command line without any options.
    sysbench 1.0.17 (using system LuaJIT 2.0.4)

    Running the test with following options:
    Number of threads: 1
    Initializing random number generator from current time


    Prime numbers limit: 20000

    Initializing worker threads...

    Threads started!

    CPU speed:
        events per second:   347.29

    General statistics:
        total time:                          10.0010s
        total number of events:              3474

    Latency (ms):
            min:                                    2.22
            avg:                                    2.88
            max:                                   36.32
            95th percentile:                        4.82
            sum:                                 9990.62

    Threads fairness:
        events (avg/stddev):           3474.0000/0.00
        execution time (avg/stddev):   9.9906/0.00
    ```

    - CPU Lúc ban đầu :

        <img src=https://i.imgur.com/r1psQ9y.png>

    - CPU lúc sau khi đẩy tải :

        <img src=https://i.imgur.com/pfDpU5l.png>

### **2.2) Benchmark FileIO**
- **B1 :** Sử dụng lệnh sau để tạo 1 file lớn hơn RAM nhiều lần (`10GB`) :
    ```
    # sysbench --test=fileio --file-total-size=10G prepare
    ```
    ```
    WARNING: the --test option is deprecated. You can pass a script name or path on the command line without any options.
    sysbench 1.0.17 (using system LuaJIT 2.0.4)

    128 files, 81920Kb each, 10240Mb total
    Creating files for the test...
    Extra file open flags: (none)
    Creating file test_file.0
    Creating file test_file.1
    Creating file test_file.2
    Creating file test_file.3
    .......
    10737418240 bytes written in 16.19 seconds (632.39 MiB/sec).
    ```
- **B2 :** Chạy các file benchmark :
    ```
    # sysbench --test=fileio --file-total-size=10G --file-test-mode=rndrw --time=300 --max-requests=0 run
    ```
    ```
    WARNING: the --test option is deprecated. You can pass a script name or path on the command line without any options.
    sysbench 1.0.17 (using system LuaJIT 2.0.4)

    Running the test with following options:
    Number of threads: 1
    Initializing random number generator from current time


    Extra file open flags: (none)
    128 files, 80MiB each
    10GiB total file size
    Block size 16KiB
    Number of IO requests: 0
    Read/Write ratio for combined random IO test: 1.50
    Periodic FSYNC enabled, calling fsync() each 100 requests.
    Calling fsync() at the end of test, Enabled.
    Using synchronous I/O mode
    Doing random r/w test
    Initializing worker threads...

    Threads started!


    File operations:
        reads/s:                      3291.11
        writes/s:                     2194.07
        fsyncs/s:                     7021.14

    Throughput:
        read, MiB/s:                  51.42
        written, MiB/s:               34.28

    General statistics:
        total time:                          300.0072s
        total number of events:              3752041

    Latency (ms):
            min:                                    0.00
            avg:                                    0.08
            max:                                   29.19
            95th percentile:                        0.28
            sum:                               297240.57

    Threads fairness:
        events (avg/stddev):           3752041.0000/0.00
        execution time (avg/stddev):   297.2406/0.00
    ```
- **B3 :** Xóa các file bench vừa tạo :
    ```
    # sysbench --test=fileio --file-total-size=10G cleanup
    ```
### **2.3) Benchmark MySQL**
- **B1 :** Tạo 1 database tên `sysbench` :

    <img src=https://i.imgur.com/HbtdByN.png>

- **B2 :** Tạo 2 table với mỗi table là `1000000` record :
    ```
    # sysbench /usr/share/sysbench/oltp_read_write.lua --mysql-host=localhost --mysql-port=3306 --mysql-user=root --mysql-password='P@ssw0rd' --mysql-db=sysbench --db-driver=mysql --tables=2 --table-size=1000000  prepare
    ```
- **B3 :** Đẩy tải **MySQL** :
    ```
    # sysbench /usr/share/sysbench/select_random_points.lua --table-size=2000000 --num-threads=100 --rand-type=uniform --db-driver=mysql --mysql-db=sysbench --mysql-user=root --mysql-password='P@ssw0rd' --time=30 run
    ```
    ```
    WARNING: --num-threads is deprecated, use --threads instead
    sysbench 1.0.17 (using system LuaJIT 2.0.4)

    Running the test with following options:
    Number of threads: 100
    Initializing random number generator from current time


    Initializing worker threads...

    Threads started!

    SQL statistics:
        queries performed:
            read:                            139582
            write:                           0
            other:                           0
            total:                           139582
        transactions:                        139582 (4640.89 per sec.)
        queries:                             139582 (4640.89 per sec.)
        ignored errors:                      0      (0.00 per sec.)
        reconnects:                          0      (0.00 per sec.)

    General statistics:
        total time:                          30.0692s
        total number of events:              139582

    Latency (ms):
            min:                                    0.20
            avg:                                   21.50
            max:                                 3265.55
            95th percentile:                       33.12
            sum:                              3001563.29

    Threads fairness:
        events (avg/stddev):           1395.8200/328.07
        execution time (avg/stddev):   30.0156/0.01
    ```
- **B4 :** Dọn dẹp DB sau khi test xong :
    ```
    # sysbench /usr/share/sysbench/oltp_read_write.lua --db-driver=mysql --mysql-db=sysbench --mysql-user=root --mysql-password='P@ssw0rd' --tables=2 cleanup
    ```
    ```
    sysbench 1.0.17 (using system LuaJIT 2.0.4)

    Dropping table 'sbtest1'...
    Dropping table 'sbtest2'...
    ```
