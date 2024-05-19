import subprocess
import os

def run_command(command):
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')

def install_packages():
    packages = [
        "base",
        "linux",
        "linux-firmware",
        "git",
        "python",
        "libnma",  # Add more packages as needed
    ]
    run_command(f"pacman -Sy --noconfirm {' '.join(packages)}")

def build_aur_package(pkg_name):
    run_command(f"git clone https://aur.archlinux.org/{pkg_name}.git /tmp/{pkg_name}")
    os.chdir(f"/tmp/{pkg_name}")
    run_command("makepkg -si --noconfirm")

def install_aur_packages():
    aur_packages = [
        "google-chrome"  # Add more AUR packages as needed
    ]
    for pkg in aur_packages:
        build_aur_package(pkg)

def main():
    install_packages()
    install_aur_packages()
    # Add any other necessary setup here

if __name__ == "__main__":
    main()
