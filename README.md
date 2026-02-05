## A. Setup ELK in EC2 (Ubuntu)
#### 1. Run the `setup_elk.sh` script
```bash
bash setup_elk.sh
```

#### 2. Reset password and token
```bash
#Reset User Password
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic -i

#RESET Token
sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```

---

### Helpful commands/infos
1. Sample `/etc/logstash/conf.d/test.conf`file
    ```bash
    input {
    tcp {
        port => 5044
        codec => json
    }
    }


    output {
    elasticsearch {
        hosts => ["https://localhost:9200"]
        user => "elastic"
        password => "<enter-your-password-here>"
        ssl_enabled => true
        ssl_certificate_authorities => "/etc/logstash/certs/http_ca.crt"
        index => "ribesh-app-logs-%{+YYYY.MM.dd}"
    }
    stdout { codec => rubydebug }
    }
    ```

2. Check the logs of `logstash` to verify **incoming logs**
    ```bash
    sudo journalctl -u logstash -f
    ```


    Sample Output:
    ```bash
    Feb 05 09:19:05 ip-172-31-85-0 logstash[8985]: {
    Feb 05 09:19:05 ip-172-31-85-0 logstash[8985]:       "@version" => "1",
    Feb 05 09:19:05 ip-172-31-85-0 logstash[8985]:          "level" => "ERROR",
    Feb 05 09:19:05 ip-172-31-85-0 logstash[8985]:        "message" => "Action failed: upload",
    Feb 05 09:19:05 ip-172-31-85-0 logstash[8985]:     "@timestamp" => 2026-02-05T09:19:05.438356Z,
    Feb 05 09:19:05 ip-172-31-85-0 logstash[8985]:        "service" => "ribesh-app-main"
    Feb 05 09:19:05 ip-172-31-85-0 logstash[8985]: }
    Feb 05 09:19:10 ip-172-31-85-0 logstash[8985]: [2026-02-05T09:19:10,443][INFO ][logstash.codecs.jsonlines][main][62d552f2861d01d9c4948a28782213ba8f493bc325d8c9d02f8a683b215f0b12] ECS compatibility is enabled but `target` option was not specified. This may cause fields to be set at the top-level of the event where they are likely to clash with the Elastic Common Schema. It is recommended to set the `target` option to avoid potential schema conflicts (if your data is ECS compliant or non-conflicting, feel free to ignore this message)
    Feb 05 09:19:10 ip-172-31-85-0 logstash[8985]: {
    Feb 05 09:19:10 ip-172-31-85-0 logstash[8985]:       "@version" => "1",
    Feb 05 09:19:10 ip-172-31-85-0 logstash[8985]:          "level" => "INFO",
    Feb 05 09:19:10 ip-172-31-85-0 logstash[8985]:        "message" => "Action success: upload",
    Feb 05 09:19:10 ip-172-31-85-0 logstash[8985]:     "@timestamp" => 2026-02-05T09:19:10.439618Z,
    Feb 05 09:19:10 ip-172-31-85-0 logstash[8985]:        "service" => "ribesh-app-main"
    Feb 05 09:19:10 ip-172-31-85-0 logstash[8985]: }
    Feb 05 09:19:15 ip-172-31-85-0 logstash[8985]: [2026-02-05T09:19:15,444][INFO ][logstash.codecs.jsonlines][main][62d552f2861d01d9c4948a28782213ba8f493bc325d8c9d02f8a683b215f0b12] ECS compatibility is enabled but `target` option was not specified. This may cause fields to be set at the top-level of the event where they are likely to clash with the Elastic Common Schema. It is recommended to set the `target` option to avoid potential schema conflicts (if your data is ECS compliant or non-conflicting, feel free to ignore this message)
    Feb 05 09:19:15 ip-172-31-85-0 logstash[8985]: {
    Feb 05 09:19:15 ip-172-31-85-0 logstash[8985]:       "@version" => "1",
    Feb 05 09:19:15 ip-172-31-85-0 logstash[8985]:          "level" => "ERROR",
    Feb 05 09:19:15 ip-172-31-85-0 logstash[8985]:        "message" => "Action failed: download",
    Feb 05 09:19:15 ip-172-31-85-0 logstash[8985]:     "@timestamp" => 2026-02-05T09:19:15.440904Z,
    Feb 05 09:19:15 ip-172-31-85-0 logstash[8985]:        "service" => "ribesh-app-main"
    ```
---

## Build and Run the Python Application in Docker
➡️ [Create Dummy Docker Application](app/Create%20Dummy%20Application.md)