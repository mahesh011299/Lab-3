pipeline {
    agent any
    options {
        // Prevent race conditions between concurrent builds
        disableConcurrentBuilds()
    }
    environment {
        // Using the exact Docker executable location on your machine
        DOCKER = "\"C:\\Users\\HP\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe\""
        IMAGE_NAME = "mycompany/payment"
        APP_VERSION = "2.0.0"
        DEPLOY_PORT = "8080"
    }
    stages {
        stage('Build') {
            steps {
                script {
                    def shortSha = bat(script: '@git rev-parse --short HEAD 2>nul || echo local', returnStdout: true).trim()
                    env.GIT_SHA = shortSha ? shortSha.split('\r?\n').last().trim() : "local"
                    env.IMMUTABLE_TAG = "${BUILD_NUMBER}-${env.GIT_SHA}"
                }
                echo "Building Docker Image: ${IMAGE_NAME}:${IMMUTABLE_TAG}"
                bat "${DOCKER} build -t ${IMAGE_NAME}:${IMMUTABLE_TAG} ."
            }
        }
        stage('Test') {
            steps {
                echo "Testing Docker image..."
                bat "${DOCKER} run --rm ${IMAGE_NAME}:${IMMUTABLE_TAG} python -c \"import app; print('App module verified')\""
            }
        }
        stage('Tag') {
            steps {
                echo "Tagging image with immutable tag and latest..."
                bat "${DOCKER} tag ${IMAGE_NAME}:${IMMUTABLE_TAG} ${IMAGE_NAME}:latest"
            }
        }
        stage('Push') {
            steps {
                echo "Simulating push of ${IMAGE_NAME}:${IMMUTABLE_TAG} to registry"
            }
        }
        stage('Deploy') {
            steps {
                echo "=========================================================="
                echo "Application Version : ${APP_VERSION}"
                echo "Git Commit          : ${env.GIT_SHA}"
                echo "Docker Image        : ${IMAGE_NAME}:${IMMUTABLE_TAG}"
                echo "Jenkins Build Number: ${BUILD_NUMBER}"
                echo "=========================================================="

                // Use Windows batch syntax (& verify >nul ignores stop/rm error codes if container doesn't exist)
                bat "@${DOCKER} stop payment 2>nul & verify >nul"
                bat "@${DOCKER} rm payment 2>nul & verify >nul"
                bat "${DOCKER} run -d --name payment -p ${DEPLOY_PORT}:8080 -e APP_VERSION=${APP_VERSION} -e BUILD_NUMBER=${BUILD_NUMBER} -e GIT_COMMIT=${env.GIT_SHA} ${IMAGE_NAME}:${IMMUTABLE_TAG}"
            }
        }
    }
    post {
        success {
            echo "SUCCESS: Deployed immutable release ${IMAGE_NAME}:${IMMUTABLE_TAG}"
        }
        failure {
            echo "FAILURE: Deployment failed."
        }
    }
}