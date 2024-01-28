# ysmr

Modular notification system for Logstash.

## Installation

ysmr accepts parsed SSH logs and wraps them in API calls for various purposes. The host must first be configured to pass this information to the script.

### Setup Logstash

Logstash should be configured to execute the "ysmr.py" script each time a log entry is added. Example:

```ruby
output {
  exec {
    command => "/usr/bin/python3 /ysmr/ysmr/ysmr/ysmr.py %{src_ip} %{src_port} %{login_status}"
  }
}
```