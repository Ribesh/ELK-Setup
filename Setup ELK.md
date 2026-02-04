## 1. Run the `setup_elk.sh` script
```bash
bash setup_elk.sh
```

## 2. Reset password and token
```bash
#Reset User Password
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic -i

#RESET Token
sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```
