pipeline {
    agent any
    
    options {
        timeout(time: 30, unit: 'MINUTES')
    }
    
    environment {
        PYTHON = 'python3'
        PIP = 'pip3'
    }
    
    stages {
        /*
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/ваш-пользователь/ваш-репозиторий.git',
                    credentialsId: 'ваш-credentials-id'
            }
        }
        */
        stage('Install Dependencies') {
            steps {
                script {
                    // Устанавливаем зависимости Python
                    sh "${PIP} install -r requirements.txt"
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    // Запускаем pytest
                    sh "${PYTHON} -m pytest tests/ -v --junitxml=test-results.xml"
                }
            }
            post {
                always {
                    // Сохраняем результаты тестов
                    junit 'test-results.xml'
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'All tests passed successfully!'
        }
        failure {
            echo 'Tests failed. Check the logs for details.'
        }
    }
}