#!/bin/bash

curl -X POST -F name=file -F "image=@sample.jpg" 'http://localhost:8000/v1/identify/plate?country=us'
