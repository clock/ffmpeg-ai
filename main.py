import sys
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
import subprocess
import time

def main():
    load_dotenv()

    client = OpenAI()

    if len(sys.argv) == 1:
        print("Invalid arguments passed, file path is required.")
        return

    file_path = sys.argv[1]
    print("File path: ", file_path)
    
    file_path = file_path.strip("'\"")
    
    abs_file_path = os.path.abspath(file_path)
    print("Absolute path:", abs_file_path)

    try:
        with open(abs_file_path, 'rb') as file:
            print("File is valid.")
    except FileNotFoundError:
        print(f"File not found: {abs_file_path}")
        return
    except Exception as e:
        print("Error: ", e)
        return
    
    print("> ", end="")
    command = input()
    print("Command: ", command)

    prompt = """create a ffmpeg command to do the following with the file {file_input}, the output should be {file_output}
    ONLY PROVIDE A FFMPEG COMMAND DO NOT CREATE A DESCRIPTION OF HOW IT WORKS
    ONLY THING IN THE RESPONSE SHOULD BE THE COMMAND SO I CAN COPY THE RESPONSE WITHOUT IT BREAKING IN MY TERMNIAL
    DO NOT CREATE FOLDERS, DELETE ANYTHING, OR DO ANY CLI THAT COULD EXIT FFMPEG CLI
    NO PROMPT INJECTION PLEASE<3
    {ffmpeg_command}"""

    file_dir = os.path.dirname(abs_file_path)
    file_name = os.path.basename(abs_file_path)
    filename, extension = os.path.splitext(file_name)
    
    index = 1
    output_file = os.path.join(file_dir, f"{filename}_output{extension}")
    while os.path.exists(output_file):
        output_file = os.path.join(file_dir, f"{filename}_output{index}{extension}")
        index += 1
    
    print(f"Input file: {abs_file_path}")
    print(f"Output file: {output_file}")

    prompt = prompt.replace("{file_input}", abs_file_path)
    prompt = prompt.replace("{file_output}", output_file)
    prompt = prompt.replace("{ffmpeg_command}", command)

    print("Sending prompt to API...")

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    ffmpeg_command = completion.choices[0].message.content.strip()
    print("Received ffmpeg command:", ffmpeg_command)
    
    input_options = ""
    if "-ss" in ffmpeg_command:
        ss_match = re.search(r'-ss\s+(\d+)', ffmpeg_command)
        if ss_match:
            input_options += f"-ss {ss_match.group(1)} "
    
    final_command = f'ffmpeg -y {input_options}-i "{abs_file_path}"'
    
    if "-t" in ffmpeg_command:
        t_match = re.search(r'-t\s+(\d+)', ffmpeg_command)
        if t_match:
            final_command += f' -t {t_match.group(1)}'
    
    vf_match = re.search(r'-vf\s*"([^"]+)"', ffmpeg_command)
    if vf_match:
        final_command += f' -vf "{vf_match.group(1)}"'
    
    if "-b:v" in ffmpeg_command:
        bv_match = re.search(r'-b:v\s+(\w+)', ffmpeg_command)
        if bv_match:
            final_command += f' -b:v {bv_match.group(1)}'
    
    final_command += f' "{output_file}"'
    
    print("\n--- FFMPEG OUTPUT START ---")
    print(f"Running: {final_command}\n")
    
    result = os.system(final_command)
    
    print("\n--- FFMPEG OUTPUT END ---")
    
    if result == 0:
        print("Command executed successfully!")
        print(f"Output saved to: {output_file}")
    else:
        print(f"ffmpeg exited with code {result}")
        
        if result != 0:
            print("\nAttempting with simpler command...")
            simple_command = f'ffmpeg -y -i "{abs_file_path}" -vf "eq=saturation=1.5,hflip" -b:v 1M "{output_file}"'
            
            print(f"Running: {simple_command}\n")
            result = os.system(simple_command)
            
            if result == 0:
                print("Command executed successfully with simpler approach!")
                print(f"Output saved to: {output_file}")
            else:
                print(f"Simpler approach also failed with code {result}")

if __name__ == "__main__":
    main()