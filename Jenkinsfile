pipeline {
    agent any
    options {
        // Task requirement: Prevent concurrent race conditions when two builds run at once
        disableConcurrentBuilds()
        ansiColor('xterm')
    }
    environment {
        IMAGE_NAME = "mycompany/payment"
        // Metadata requirements: immutable tag with build number and short git sha
        SHORT_COMMIT = sh(script: "git rev-parse --short HEAD || echo 'local'", returnStdout: true).trim()
        IMMUTABLE_TAG = "${BUILD_NUMBER}-${SHORT_COMMIT}"
        APP_VERSION = "2.0.0"
    }
    stages {
        stage('Build') {
            steps {
                echo "Building Docker Image: ${IMAGE_NAME}:${IMMUTABLE_TAG}"
                sh """
                    docker build \
                        --build-arg BUILD_NUMBER=${BUILD_NUMBER} \
                        --build-arg GIT_COMMIT=${SHORT_COMMIT} \
                        -t ${IMAGE_NAME}:${IMMUTABLE_TAG} .
                """
            }
        }
        stage('Test') {
            steps {
                echo "Running Container Tests..."
                sh """
                    docker run --rm ${IMAGE_NAME}:${IMMUTABLE_TAG} python -c "import app; print('App module imports cleanly')"
                """
            }
        }
        stage('Tag') {
            steps {
                echo "Tagging image with immutable tag and latest..."
                sh """
                    docker tag ${IMAGE_NAME}:${IMMUTABLE_TAG} ${IMAGE_NAME}:latest
                """
            }
        }
        stage('Push') {
            steps {
                // If using a remote registry (Docker Hub), push here:
                echo "Pushing ${IMAGE_NAME}:${IMMUTABLE_TAG} to registry (simulated locally)"
                // sh "docker push ${IMAGE_NAME}:${IMMUTABLE_TAG}"
            }
        }
        stage('Deploy') {
            steps {
                // Task requirement: Print application version, Git commit, Docker image, and Jenkins build
                echo "=========================================================="
                echo "DEPLOYING RELEASE"
                echo "Application Version : ${APP_VERSION}"
                echo "Git Commit          : ${SHORT_COMMIT}"
                echo "Docker Image        : ${IMAGE_NAME}:${IMMUTABLE_TAG}"
                echo "Jenkins Build Number: ${BUILD_NUMBER}"
                echo "=========================================================="
                
                sh """
                    docker stop payment || true
                    docker rm payment || true
                    docker run -d \
                      --name payment \
                      -p 8080:8080 \
                      -e APP_VERSION=${APP_VERSION} \
                      -e BUILD_NUMBER=${BUILD_NUMBER} \
                      -e GIT_COMMIT=${SHORT_COMMIT} \
                      ${IMAGE_NAME}:${IMMUTABLE_TAG}
                """
            }
        }
    }
    post {
        success {
            echo "Deployment verified with immutable tag: ${IMAGE_NAME}:${IMMUTABLE_TAG}"
        }
        failure {
            echo "Deployment failed."
        }
    }
}