#!/usr/bin/env python

import argparse
import os
import subprocess
import shutil
import sys

# Optimized for Debian 12 amd64
print("Detecting distro info...")
subprocess.run(["uname","-a"])

# Default values
DEFAULT_MODEL_URL = "https://gpt4all.io/models/ggml-gpt4all-l13b-snoozy.bin"  
PROJECTS = ["LocalAI", "Auto-GPT"]
AUTO_GPT_BRANCH = "stable"

# Argument parsing
parser = argparse.ArgumentParser(description="Manage LocalAI and Auto-GPT projects.")
parser.add_argument("--custom_model_url", type=str,
                    help="Specify a custom URL for the model download step.")
parser.add_argument("--uninstall", action="store_true",
                    help="Uninstall the projects from your local machine.")
args = parser.parse_args()

model_url = args.custom_model_url if args.custom_model_url else DEFAULT_MODEL_URL

# Handle uninstall
if args.uninstall:
    print("Uninstalling...")
    for project in PROJECTS:
        if os.path.isdir(project):
            shutil.rmtree(project)
    sys.exit(0)
            
# Install prerequisites
print("Installing prerequisites...")
subprocess.run(["sudo", "apt", "update"])
subprocess.run(["sudo", "apt", "install", "-y", "git", "cmake", "golang-go"])

# Configure git
subprocess.run(["git", "config", "--global", "user.name", "'myusername'"])
subprocess.run(["git", "config", "--global", "user.email", "'my@email.com'"])

# Set environment variables for amd64
os.environ["GOOS"] = "linux"
os.environ["GOARCH"] = "amd64"

# Handle LocalAI
if not os.path.isdir("LocalAI"):
    subprocess.run(["git", "clone", "https://github.com/go-skynet/LocalAI"])
else:
    os.chdir("LocalAI")
    subprocess.run(["git", "pull"])
    os.chdir("..")
    
os.chdir("LocalAI")
subprocess.run(["make", "build"])
os.chdir("..") 

# Download model if needed  
if not shutil.which("wget"):
    subprocess.run(["sudo", "apt", "install", "-y", "wget"])

if args.custom_model_url or not os.path.isfile("LocalAI/models/gpt-3.5-turbo"):
    subprocess.run(["wget", model_url, "-O", "LocalAI/models/gpt-3.5-turbo"])

# Handle Auto-GPT  
if not os.path.isdir("Auto-GPT"):
    subprocess.run(["git", "clone", "-b", AUTO_GPT_BRANCH, "https://github.com/Significant-Gravitas/Auto-GPT.git"])
    shutil.copy(".env.template", "Auto-GPT/.env")
else:
    os.chdir("Auto-GPT")
    subprocess.run(["git", "pull"]) 
    os.chdir("..")
