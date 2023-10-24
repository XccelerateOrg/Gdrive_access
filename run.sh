#!/bin/bash

docker run -p 80:5001 -v ./models:/gdrive/models -v ./oauth_key:/gdrive/oauth_key -it --rm gdrive_app bash