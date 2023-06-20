# LLM Demo

## Deploying the Flask WebApp to GCP Cloud Run:

```
gcloud auth login
gcloud config set project xebia-ai-training
gcloud auth configure-docker 
docker buildx build . --platform linux/amd64 -t yourname-gcp-demo
docker tag yourname-gcp-demo gcr.io/xebia-ai-training/yourname-gcp-demo
docker push gcr.io/xebia-ai-training/yourname-gcp-demo
gcloud run deploy yourname-gcp-demo \
  --image gcr.io/xebia-ai-training/yourname-gcp-demo \
  --platform managed --region us-east1 --allow-unauthenticated
```

## Local testing

```
python3 app.py
```


