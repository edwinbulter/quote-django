pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the Django project repository...'
                git 'https://github.com/edwinbulter/quote-django.git'  // Replace with your Git repo
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Building the Docker image...'
                script {
                    // Use a unique Docker image tag, like the build number
                    def imageTag = "django-app:${env.BUILD_NUMBER}"
                    env.IMAGE_TAG = imageTag  // Export the tag for later stages

                    // Build the Docker image
                    sh "docker build -t ${imageTag} ."
                }
            }
        }
        stage('Run Container') {
            steps {
                echo 'Running the container...'
                script {
                    // Stop and remove any old container if running
                    sh """
                    docker ps -q --filter "name=quote-django" | xargs -r docker stop
                    docker ps -aq --filter "name=quote-django" | xargs -r docker rm
                    """

                    // Run the container on port 8002 (or another port)
                    sh """
                    docker run -d --name quote-django -p 8002:8002 ${env.IMAGE_TAG}
                    """
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline execution completed.'
        }
        failure {
            echo 'Pipeline failed. Cleaning up...'
            // Remove any dangling containers/images
            sh """
            docker ps -aq --filter "name=quote-django" | xargs -r docker rm
            docker image prune -f
            """
        }
    }
}