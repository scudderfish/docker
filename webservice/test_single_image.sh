#!/bin/bash

curl -X POST -F name=file -F "image=@sample.jpg" 'https://localhost:8888/v1/identify/plate?country=us'
