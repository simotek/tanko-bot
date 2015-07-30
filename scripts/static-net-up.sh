#!/bin/bash
nmcli con add con-name eth0-static ifname enp0s20 type ethernet ip4 192.168.101.2/24 gw4 192.168.101.1

