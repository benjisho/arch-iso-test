pipeline {
    agent any
    environment {
        PACKER_VM_IP = '10.8.112.3' // the IP of the packer machine.
        GIT_REPO_URL = 'https://github.com/benjisho/arch-iso-test.git' // the git that we are testing
        BRANCH_NAME = 'main' // the branch in that git that we are testing.
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
                    def timestamp = new Date().format("yyyyMMddHHmmss")
                    def outputDir = "output-${timestamp}"
                    
                    sshagent(['github-ssh-key']) {
                        sh """
                            ssh root@${PACKER_VM_IP} "rm -rf /tmp/arch-iso-test || true"
                            ssh root@${PACKER_VM_IP} "git clone ${GIT_REPO_URL} /tmp/arch-iso-test"
                            ssh root@${PACKER_VM_IP} "packer --version && packer plugins installed"
                            ssh root@${PACKER_VM_IP} "bash /opt/packer/fetch_checksum.sh"
                            ISO_CHECKSUM=\$(ssh root@${PACKER_VM_IP} "cat /tmp/iso_checksum.txt")
                            echo "ISO_CHECKSUM=\$ISO_CHECKSUM"
                            ssh root@${PACKER_VM_IP} "cd /opt/packer && packer build -var 'iso_checksum=\$ISO_CHECKSUM' -var 'output_dir=${outputDir}' arch-iso.json"
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
                script {
                    def timestamp = new Date().format("yyyyMMddHHmmss")
                    def outputDir = "output-${timestamp}"
                    
                    sshagent(['github-ssh-key']) {
                        sh "scp root@${PACKER_VM_IP}:/opt/packer/${outputDir}/*.iso ./"
                    }
                }
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts: '*.iso', allowEmptyArchive: true // store the iso file locally of the jenkins.
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