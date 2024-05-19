import os

def install_packages():
    # Update package database and upgrade system
    os.system('pacman -Syu --noconfirm')

    # Install official packages
    official_packages = [
        'libnma',  # Example package
        # Add other official packages here
    ]
    os.system(f'pacman -Sy --noconfirm {" ".join(official_packages)}')

    # Install AUR helper (yay)
    os.system('pacman -Sy --noconfirm base-devel git')
    os.system('git clone https://aur.archlinux.org/yay.git /tmp/yay')
    os.chdir('/tmp/yay')
    os.system('makepkg -si --noconfirm')

    # Install AUR packages
    aur_packages = [
        'google-chrome',  # Example package
        # Add other AUR packages here
    ]
    os.system(f'yay -S --noconfirm {" ".join(aur_packages)}')

if __name__ == "__main__":
    install_packages()
