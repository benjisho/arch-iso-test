pipeline {
    agent any
    environment {
        PACKER_VM_IP = '10.8.112.3' // the IP of the Packer VM
        GIT_REPO_URL = 'https://github.com/benjisho/arch-iso-test.git' // the git repo we are testing
        BRANCH_NAME = 'main' // the branch in the git repo we are testing
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
                    def sshPublicKey = sh(script: 'cat ~/.ssh/id_rsa.pub', returnStdout: true).trim()
                    
                    sshagent(['github-ssh-key']) {
                        sh """
                            ssh root@${PACKER_VM_IP} "rm -rf /tmp/arch-iso-test || true"
                            ssh root@${PACKER_VM_IP} "git clone ${GIT_REPO_URL} /tmp/arch-iso-test"
                            ssh root@${PACKER_VM_IP} "packer --version && packer plugins installed"
                            ssh root@${PACKER_VM_IP} "bash /opt/packer/fetch_checksum.sh"
                            ISO_CHECKSUM=\$(ssh root@${PACKER_VM_IP} "cat /tmp/iso_checksum.txt")
                            echo "ISO_CHECKSUM=\$ISO_CHECKSUM"

                            ssh root@${PACKER_VM_IP} "rm -f /tmp/packer_qemu_ssh_key /tmp/packer_qemu_ssh_key.pub"
                            ssh root@${PACKER_VM_IP} "ssh-keygen -t rsa -b 4096 -f /tmp/packer_qemu_ssh_key -N ''"
                            ssh root@${PACKER_VM_IP} "chmod 600 /tmp/packer_qemu_ssh_key"
                            QEMU_SSH_PUBLIC_KEY=\$(ssh root@${PACKER_VM_IP} "cat /tmp/packer_qemu_ssh_key.pub")
                            echo "QEMU_SSH_PUBLIC_KEY=\$QEMU_SSH_PUBLIC_KEY"
                            
                            ssh root@${PACKER_VM_IP} "cd /opt/packer && PACKER_LOG=1 packer build -var 'iso_checksum=\$ISO_CHECKSUM' -var 'output_dir=${outputDir}' -var 'ssh_public_key=\$QEMU_SSH_PUBLIC_KEY' arch-iso.json"
                            
                            ssh root@${PACKER_VM_IP} "cat /tmp/packer.log"
                        """
                    }
                }
            }
        }
        stage('Copy Packer ISO') {
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
        stage('Build Custom ISO') {
            steps {
                script {
                    def outputDir = "custom-iso-output"
                    
                    sshagent(['github-ssh-key']) {
                        sh """
                            ssh root@${PACKER_VM_IP} "
                            cp -r /usr/share/archiso/configs/releng /tmp/customiso &&
                            cp /tmp/arch-iso-test/airootfs/root/customize_airootfs.sh /tmp/customiso/airootfs/root/ &&
                            cp /tmp/arch-iso-test/pacman.conf /tmp/customiso/ &&
                            mkarchiso -v -w /tmp/customiso/work -o /tmp/customiso/out /tmp/customiso
                            "
                        """
                    }
                }
            }
        }
        stage('Copy Custom ISO') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    sshagent(['github-ssh-key']) {
                        sh "scp root@${PACKER_VM_IP}:/tmp/customiso/out/*.iso ./"
                    }
                }
            }
        }
        stage('Shutdown VM') {
            steps {
                sshagent(['github-ssh-key']) {
                    sh "ssh root@${PACKER_VM_IP} 'shutdown -P now'"
                }
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts: '*.iso', allowEmptyArchive: true // store the iso files locally on Jenkins
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
