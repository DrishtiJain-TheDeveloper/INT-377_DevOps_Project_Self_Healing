pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "huntrixx"
        BACKEND_IMAGE = "huntrixx/ocean-backend:latest"
        FRONTEND_IMAGE = "huntrixx/ocean-frontend:latest"
    }

    stages {

        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/DrishtiJain-TheDeveloper/INT-377_DevOps_Project_Self_Healing',
                    branch: 'main'
            }
        }

        stage('Build Images') {
            steps {
                sh """
                    docker build -t $BACKEND_IMAGE ./backend
                    docker build -t $FRONTEND_IMAGE ./frontend
                """
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-pass', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                sh '''
                echo $PASS | docker login -u $USER --password-stdin'''
                    
                }
            }
        }

        stage('Push Images') {
            steps {
                sh """
                    docker push $BACKEND_IMAGE
                    docker push $FRONTEND_IMAGE
                """
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f k8s/"
                sh "kubectl rollout restart deployment backend-deployment"
                sh "kubectl rollout restart deployment frontend-deployment"
            }
        }

        stage('Verify') {
            steps {
                sh """
                    kubectl get pods
                    kubectl get svc
                """
            }
        }
        stage('Deploy Monitoring') {
            steps {
                sh 'kubectl apply -f monitoring/'
                }
        }
    }
}