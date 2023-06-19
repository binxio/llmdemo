# LLM Demo

## Deploying the Flask WebApp to GCP Cloud Run:

```
gcloud auth login
gcloud config set project xebia-ai-training
gcloud auth configure-docker 
docker buildx build . --platform linux/amd64 -t gcp-llm
docker tag gcp-llm gcr.io/xebia-ai-training/gcp-llm
docker push gcr.io/xebia-ai-training/gcp-llm
gcloud run deploy gcp-llm \
  --image gcr.io/xebia-ai-training/gcp-llm \
  --platform managed --region us-east1 --allow-unauthenticated
```

Note that you might need to configure the API key as an environment variable.

## Local testing

```
python3 app.py
```


