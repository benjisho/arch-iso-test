pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-repo.git'
            }
        }
        stage('Build Image') {
            steps {
                sh 'ssh user@packer_vm_ip "cd /path/to/packer && packer build packer.json"'
            }
        }
    }
}
