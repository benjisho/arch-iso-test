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
        stage('Copy ISO') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sshagent(['packer-ssh-key']) {
                    sh "scp root@${PACKER_VM_IP}:/tmp/arch-installer/output/*.iso ./"
                }
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts: '*.iso', allowEmptyArchive: true
        }
        failure {
            script {
                def logContent = sh(script: "ssh root@${PACKER_VM_IP} 'cat /tmp/install.log'", returnStdout: true).trim()
                echo "Build failed. Error log: ${logContent}"
            }
            archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
        }
    }
}
