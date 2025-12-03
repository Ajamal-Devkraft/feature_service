pipeline {
    agent any
    stages {

        stage("Building docker image") {
            steps {
                echo "Building the Docker image"
                sh "docker build -t feature-service-2:latest ."
            }
        }

        stage('Push to GAR') {
        steps {
            withCredentials([file(credentialsId: 'gcp-sa-json', variable: 'GCLOUD_AUTH')]) {
                sh """
                    gcloud auth activate-service-account --key-file=$GCLOUD_AUTH
                    gcloud auth configure-docker asia-south1-docker.pkg.dev --quiet
                    PROJECT_ID=\$(gcloud config get-value project)
                    docker tag feature-service-2:latest asia-south1-docker.pkg.dev/\$PROJECT_ID/hdfclife/feature-service-2:latest
                    docker push asia-south1-docker.pkg.dev/\$PROJECT_ID/hdfclife/feature-service-2:latest
                """
                }
            }
        }


    }
}