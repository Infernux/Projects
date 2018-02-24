#!/bin/sh

protocol='pop3'
log='USER '$1
pass='PASS '$2
server=$3

issueCommand() {
    echo "$1"
    sleep 1;
}

#{ echo "$log"; sleep 1; echo "$pass"; sleep 1; echo "LIST"; sleep 1;} | telnet $server $protocol
output=\
`{ issueCommand "$log";  \
  issueCommand "$pass"; \
  issueCommand "LIST";  \
} | telnet $server $protocol 2> /dev/null`

echo "$output" | tail -n2 | head -n1 | cut -d' ' -f1
