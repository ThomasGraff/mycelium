#!/bin/bash

set -e  # Exit on error

echo "🔍 Checking and installing dependencies..."

# Function to check if a command exists
check_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        return 1
    fi
    return 0
}

# Function to install package based on the OS
install_package() {
    local package_name="$1"
    local package_manager=""
    local install_command=""

    if [ -f "/etc/debian_version" ]; then
        package_manager="apt-get"
        install_command="sudo apt-get install -y"
    elif [ -f "/etc/redhat-release" ]; then
        package_manager="yum"
        install_command="sudo yum install -y"
    elif [ -f "/etc/arch-release" ]; then
        package_manager="pacman"
        install_command="sudo pacman -S --noconfirm"
    elif command -v brew >/dev/null 2>&1; then
        package_manager="brew"
        install_command="brew install"
    else
        echo "❌ Unsupported package manager. Please install $package_name manually."
        return 1
    fi

    echo "💡 Installing $package_name using $package_manager..."
    $install_command "$package_name"
}

# Required dependencies
dependencies=(
    "curl"
    "jq"
    "openssl"
    "sed"
)

# Check Python and Poetry
check_python() {
    if ! check_command "python3"; then
        echo "❌ Python 3 is not installed"
        install_package "python3"
    else
        echo "✅ Python 3 is installed"
    fi

    
    if ! check_command "pip3"; then
        echo "❌ pip3 is not installed"
        install_package "python3-pip"
    else
        echo "✅ pip3 is installed"
    fi

    # Install or upgrade Poetry
    if ! check_command "poetry"; then
        echo "💡 Installing Poetry..."
        curl -sSL https://install.python-poetry.org | python3 -
    else
        echo "✅ Poetry is installed"
    fi
}

# Check Yarn
check_yarn() {
    if ! check_command "yarn"; then
        echo "💡 Installing Yarn..."
        npm install -g yarn
    else
        echo "✅ Yarn is installed"
    fi
}

# Main installation process
main() {
    
    for dep in "${dependencies[@]}"; do
        if ! check_command "$dep"; then
            echo "❌ $dep is not installed"
            install_package "$dep"
        else
            echo "✅ $dep is installed"
        fi
    done

    # Check Python environment."
    check_python

    # Check Yarn
    check_yarn

    # Verify Docker is running
    if ! docker info >/dev/null 2>&1; then
        echo "❌ Docker daemon is not running"
        echo "🔧 Please start Docker daemon and try again"
        exit 1
    else
        echo "✅ Docker daemon is running"
    fi

    echo "✅ All dependencies are installed and ready!"
}

main
