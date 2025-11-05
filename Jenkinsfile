pipeline {
  agent any

  environment {
    IMAGE = "harsh3928/automated_weather"
    TAG = "${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        sh "docker build -t ${IMAGE}:${TAG} ."
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'echo "$PASS" | docker login -u "$USER" --password-stdin'
          sh "docker push ${IMAGE}:${TAG}"
        }
      }
    }

    stage('Cleanup') {
      steps {
        sh "docker rmi ${IMAGE}:${TAG} || true"
      }
    }
  }
}
