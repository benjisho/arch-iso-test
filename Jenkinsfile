pipeline {
    agent any
    environment {
        PACKER_VM_IP = '10.8.112.3'
        GIT_REPO_URL = 'https://github.com/benjisho/arch-iso-test.git'
        BRANCH_NAME = 'main'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: "${BRANCH_NAME}", url: "${GIT_REPO_URL}"
            }
        }
        stage('Build Image') {
            steps {
                script {
                    sshagent(['github-ssh-key']) {
                        sh """
                            ssh root@${PACKER_VM_IP} "rm -rf /tmp/arch-iso-test || true"
                            ssh root@${PACKER_VM_IP} "git clone ${GIT_REPO_URL} /tmp/arch-iso-test"
                            ssh root@${PACKER_VM_IP} "cd /opt/packer && packer build arch-iso.json"
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
                sshagent(['github-ssh-key']) {
                    sh "scp root@${PACKER_VM_IP}:/opt/packer/output/*.iso ./"
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
