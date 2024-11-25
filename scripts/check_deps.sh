#!/bin/bash

set -e  # Exit on error

# Function to check if a command exists
check_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        return 1
    fi
    return 0
}

# Function to check package manager
detect_package_manager() {
    if [ -f "/etc/debian_version" ]; then
        echo "apt-get"
    elif [ -f "/etc/redhat-release" ]; then
        echo "yum"
    elif [ -f "/etc/arch-release" ]; then
        echo "pacman"
    elif command -v brew >/dev/null 2>&1; then
        echo "brew"
    else
        echo "unknown"
    fi
}

# Development dependencies check
check_dev_dependencies() {
    echo "💡 Checking development dependencies..."
    local missing_deps=()

    # Check Python environment
    if ! check_command "python3"; then
        missing_deps+=("python3")
    else
        echo "✅ Python 3 is installed"
    fi

    if ! check_command "pip3"; then
        missing_deps+=("pip3")
    else
        echo "✅ pip3 is installed"
    fi

    if ! check_command "poetry"; then
        missing_deps+=("poetry")
    else
        echo "✅ Poetry is installed"
    fi

    if ! check_command "yarn"; then
        missing_deps+=("yarn")
    else
        echo "✅ Yarn is installed"
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo "⚠️ Missing development dependencies: ${missing_deps[*]}"
        echo "💡 Please install these dependencies before proceeding with development"
        exit 1
    fi
}

# Production dependencies check
check_prod_dependencies() {
    echo "💡 Checking production dependencies..."
    local missing_deps=()
    local pkg_manager=$(detect_package_manager)

    # Required system packages
    local required_packages=(
        "curl"
        "jq"
        "openssl"
        "sed"
    )

    for dep in "${required_packages[@]}"; do
        if ! check_command "$dep"; then
            missing_deps+=("$dep")
        else
            echo "✅ $dep is installed"
        fi
    done

    # Check Docker
    if ! check_command "docker"; then
        missing_deps+=("docker")
    else
        echo "✅ Docker is installed"
        
        # Check if Docker daemon is running
        if ! docker info >/dev/null 2>&1; then
            echo "⚠️ Docker daemon is not running"
            exit 1
        else
            echo "✅ Docker daemon is running"
        fi
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo "⚠️ Missing production dependencies: ${missing_deps[*]}"
        if [ "$pkg_manager" != "unknown" ]; then
            echo "💡 You can install them using your package manager ($pkg_manager) but you might need to install them manually"
        else
            echo "⚠️ Couldn't detect package manager. Please install the dependencies manually"
        fi
        exit 1
    fi
}

# Main function
main() {
    case "$1" in
        "dev")
            check_dev_dependencies
            ;;
        "deploy"|"prod")
            check_prod_dependencies
            ;;
        "all")
            check_dev_dependencies
            echo ""
            check_prod_dependencies
            ;;
        *)
            echo "⚠️ Usage: $0 [dev|prod|all]"
            echo "💡 Example: $0 dev  - Check development dependencies"
            echo "💡 Example: $0 prod - Check production dependencies"
            echo "💡 Example: $0 all  - Check all dependencies"
            exit 1
            ;;
    esac
}

main "$1" 