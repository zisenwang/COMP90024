#!/bin/bash

ansible-playbook -i ../config/inventory/hosts -u ubuntu --key-file=~/.ssh/COMP90024.pem stop-crawler.yaml