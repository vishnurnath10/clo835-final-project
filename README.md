# CLO835 Final Project: 2-Tiered Web App Deployment on Amazon EKS

## 🎯 Project Objective

Deploy an enhanced version of the `simple-web-mysql` Flask application using Amazon EKS with a complete CI/CD pipeline, pod auto-scaling, persistent storage, and secure access to private resources.

---

## 📦 Features & Requirements

- Enhanced HTML interface with background image loaded from **private S3 bucket**
- **MySQL database** as backend with credentials managed via **Kubernetes Secrets**
- Use of **ConfigMap** for configurable environment values (background image URL, group name/slogan)
- Dockerized Flask application listening on **port 81**
- GitHub Actions pipeline to:
  - Build and test the application image
  - Push image to **Amazon ECR**
- Kubernetes manifests to:
  - Deploy **MySQL** with **PersistentVolume**
  - Deploy **Flask app** from ECR image
  - Expose Flask app to Internet using a stable endpoint
- App should recover state and retain data after pod restart
- Support for live configuration update (background image URL in ConfigMap)

---

## 🛠️ Tools & Services Used

- **Flask** and **MySQL**
- **Docker** and **GitHub Actions**
- **Amazon EKS**, **ECR**, **S3**, and **EBS**
- **kubectl**, **eksctl**
- **AWS IAM**, **Secrets Manager**

---

## 📁 Repository Structure

