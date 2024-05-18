pipeline {
    agent any
    environment {
        PACKER_VM_IP = '10.8.112.3'
        GIT_REPO_URL = 'https://github.com/benjisho/arch-iso-test'
    }
    stages {
        stage('Checkout') {
            steps {
                git url: "${GIT_REPO_URL}"
            }
        }
        stage('Build Image') {
            steps {
                script {
                    sshagent(['packer-ssh-key']) {
                        sh """
                            ssh root@${PACKER_VM_IP} "rm -rf /tmp/arch-iso-test || true"
                            ssh root@${PACKER_VM_IP} "git clone ${GIT_REPO_URL} /tmp/arch-iso-test"
                            ssh root@${PACKER_VM_IP} "cd /tmp/arch-iso-test && packer build packer.json"
                        """
                    }
                }
            }
        }
