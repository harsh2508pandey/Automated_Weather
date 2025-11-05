# 🌦️ Weather App - Full DevOps Version

This project implements a complete DevOps pipeline for a Weather App using **Docker**, **Terraform**, **Ansible**, and **GitHub Actions**.

## ⚙️ Tools Used
- Docker for containerization
- Terraform for AWS infrastructure
- Ansible for server configuration
- GitHub Actions for CI/CD automation

## 🚀 Deployment Flow
1. Push code to GitHub → triggers CI/CD workflow.
2. Docker builds and pushes image to DockerHub.
3. Ansible deploys the image on AWS EC2 (created by Terraform).
