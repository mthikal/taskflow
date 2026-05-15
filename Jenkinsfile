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
                  # Build the image
                  docker build -t taskflow-app .

                  # Stop and remove the old container if it exists
                  docker stop taskflow-container || true
                  docker rm taskflow-container || true

                  # Run the new container
                  docker run -d \
                      -p 5000:5000 \
                      --name taskflow-container \
                      taskflow-app
              '''
          }
      }
    }
}
