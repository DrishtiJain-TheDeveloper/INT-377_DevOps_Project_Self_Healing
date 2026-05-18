pipeline {
    agent { label 'WORKER_NODE_01' }

    stages {
        stage('Clone_Code_From_Repository_on Github') {
            steps {
                echo 'Cloning code from GitHub...'
                git url: 'https://github.com/DrishtiJain-TheDeveloper/Jenkins_Pepeline_basic',
                    branch: 'main'
            }
        }

        stage('Stop Old Containers') {
            steps {
                sh 'docker compose down || true'
            }
        }

        stage('Build New Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Start Containers') {
            steps {
                sh 'docker compose up -d'
            }
        }
        stage('Verify Running Containers') {
            steps {
                sh 'docker ps'
            }
        }
    }
}