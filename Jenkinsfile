pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv env
                    . env/bin/activate
                    pip install -r requirements.txt -q
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    . env/bin/activate
                    pytest
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    . env/bin/activate
                    gunicorn --bind 0.0.0.0:5000 wsgi:app --daemon \
                        --pid /tmp/taskflow.pid \
                        --access-logfile /tmp/taskflow-access.log
                    echo "App running on http://localhost:5000"
                '''
            }
        }
    }
}
