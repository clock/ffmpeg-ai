    import os
    import subprocess
    import sys
    import shutil

    def print_current_path():
        """Prints the current PATH environment variable."""
        print("\nCurrent PATH:\n" + os.environ["PATH"].replace(os.pathsep, "\n"))

    def is_ffmpeg_in_system_path():
        """Checks if ffmpeg is actually available in the system PATH."""
        try:
            # Get absolute path of ffmpeg
            ffmpeg_path = shutil.which("ffmpeg")
            if not ffmpeg_path:
                print("ffmpeg not found in PATH")
                return False
                
            # Convert to absolute path to check if it's in current directory
            ffmpeg_abs = os.path.abspath(ffmpeg_path)
            current_dir = os.path.abspath(os.getcwd())
            
            # Check if ffmpeg is in current directory (not in system PATH)
            if ffmpeg_abs.startswith(current_dir):
                print(f"Found ffmpeg at: {ffmpeg_path} (current directory only, not in system PATH)")
                return False
            else:
                print(f"Found ffmpeg in system PATH: {ffmpeg_path}")
                return True
                
        except Exception as e:
            print(f"Exception when checking ffmpeg: {e}")
            return False

    def add_ffmpeg_to_path():
        """Adds the script's directory (where ffmpeg.exe is located) to PATH if missing."""
        script_dir = os.path.abspath(os.path.dirname(__file__))
        ffmpeg_path = os.path.join(script_dir, "ffmpeg.exe")

        print("\nBefore adding ffmpeg:")
        print_current_path()
        
        # First verify if ffmpeg is actually in system PATH
        print("\nChecking if ffmpeg is already in system PATH...")
        if is_ffmpeg_in_system_path():
            print("\nffmpeg is already in system PATH.")
            return

        # If ffmpeg.exe exists in the script's directory, add it to PATH
        if os.path.exists(ffmpeg_path):
            print(f"\nFound ffmpeg.exe in: {script_dir}")
            print(f"Full path: {ffmpeg_path}")

            # Temporarily add to PATH (for this session)
            os.environ["PATH"] = script_dir + os.pathsep + os.environ["PATH"]  # Add to beginning of PATH
            
            # Persistently add to PATH
            current_path = os.environ.get("PATH", "")
            
            # Make sure we don't add duplicates to PATH
            path_parts = current_path.split(os.pathsep)
            if script_dir not in path_parts:
                # The PATH variable has a maximum length in Windows (2048 characters)
                # Let's check if adding our path would exceed this limit
                new_path = script_dir + os.pathsep + current_path
                
                print(f"Adding to system PATH permanently: {script_dir}")
                try:
                    # We need to use cmd.exe to run setx properly
                    cmd = f'setx PATH "{script_dir};%PATH%"'
                    print(f"Running command: {cmd}")
                    
                    process = subprocess.run(
                        cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    if process.returncode == 0:
                        print("Successfully updated system PATH.")
                        print(f"Command output: {process.stdout}")
                        print("IMPORTANT: You must restart your command prompt/terminal for the change to take effect.")
                    else:
                        print(f"Error updating system PATH. Return code: {process.returncode}")
                        print(f"Error output: {process.stderr}")
                        print(f"Standard output: {process.stdout}")
                except Exception as e:
                    print(f"Exception when updating PATH: {e}")
            else:
                print(f"Directory {script_dir} is already in PATH, but ffmpeg is not accessible.")
                print("This may indicate an issue with file permissions or PATH ordering.")
        else:
            print(f"\nError: ffmpeg.exe not found in the script directory: {script_dir}")
            # Look for ffmpeg.exe elsewhere in current directory
            for file in os.listdir(script_dir):
                if "ffmpeg" in file.lower():
                    print(f"Found similar file: {file}")

        print("\nAfter modifying PATH:")
        print_current_path()

    def install_requirements():
        """Installs dependencies from requirements.txt."""
        try:
            requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
            if os.path.exists(requirements_path):
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
                print("\nAll dependencies installed successfully!")
            else:
                print(f"\nWarning: requirements.txt not found at {requirements_path}")
        except subprocess.CalledProcessError as e:
            print(f"\nFailed to install dependencies: {e}")

    if __name__ == "__main__":
        add_ffmpeg_to_path()
        install_requirements()