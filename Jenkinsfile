pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        API_URL = 'http://172.20.0.1:5000'
    }

    stages {
        stage('Descargar repositorio') {
            steps {
                checkout scm
            }
        }

        stage('Preparar entorno Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Ejecutar pruebas API') {
            steps {
                sh '.venv/bin/pytest api -v --junitxml=resultado-pytest.xml'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true,
                  testResults: 'resultado-pytest.xml'
        }

        success {
            echo 'Las pruebas de la API finalizaron correctamente.'
        }

        failure {
            echo 'El pipeline falló. Revisar los resultados.'
        }
    }
}
