# Email Triage OpenEnv

## Description
This environment simulates email classification and response generation.

## Actions
- classify
- reply
- ignore

## Observation
- list of emails
- processed count

## Tasks
- Easy: classify emails
- Medium: generate responses
- Hard: optimize overall reward

## Setup
docker build -t email-env .
docker run -p 8000:8000 email-env

## Run
python inference.py