# Hackathon 4.0

## AI / Generative AI Project

This repository contains work from my hackathon projects and experimentation.

### Portfolio

My broader portfolio focuses on:

- Generative AI applications
- RAG pipelines
- LLM orchestration
- Machine Learning
- Computer Vision
- FastAPI backends
- React applications

## Highlight

I have also built and demoed a live Generative AI prototype in a **24-hour hackathon**, with the project receiving **1st place among 200+ teams** at SRM Builds 2.0 (AI domain), as listed on my resume.

## Technologies

**Python · Generative AI · LLMs · Machine Learning · React · FastAPI**

## Local configuration

The NebulaSource desktop application in `finalmain.py` reads its database
configuration from environment variables. To configure it without committing
credentials:

1. Copy `.env.example` to a local `.env` file.
2. Replace the placeholder values with your local database settings.
3. Export the values in your shell or use an environment loader before running
   the application.

Required variables: `NEBULA_DB_HOST`, `NEBULA_DB_USER`,
`NEBULA_DB_PASSWORD`, `NEBULA_DB_NAME`, and
`NEBULA_DEFAULT_PASSWORD`.

The `.env` file is intentionally ignored by Git. Never commit passwords,
database credentials, or other secrets.

More project-specific implementation details will be documented here as the repository evolves.
