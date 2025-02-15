#!/bin/bash

# Check if Django Server is running
curl localhost:8000/health || exit 1

exit 0
