#!/usr/bin/env python3
import subprocess
import time
import signal
import os

def run_frida(commands, timeout_seconds=20):
    for i, cmd in enumerate(commands, 1):
        print(f"\n{'='*50}")
        print(f"Running command {i}/{len(commands)}: {cmd}")
        print(f"{'='*50}")
        
        process = None
        try:
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                preexec_fn=os.setsid
            )
            start_time = time.time()
            try:
                return_code = process.wait(timeout=timeout_seconds)
                end_time = time.time()
                elapsed = end_time - start_time
                
                if return_code == 0:
                    print(f"Frida-trace ended after {elapsed} seconds")
                else:
                    print(f"Frida-trace crashed after {elapsed} seconds")
                    
            except subprocess.TimeoutExpired:
                print(f"Closing...")
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)    
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        # Force kill if process does not responde (happened more than once)
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                        process.wait()
  
                except ProcessLookupError:
                    print("Process already terminated")
        except FileNotFoundError:
            print(f"Error: {cmd}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=1)
                except:
                    try:
                        process.kill()
                    except:
                        pass
        
        time.sleep(2)

if __name__ == "__main__":
    target_app = "fr.vinted"
    syscalls = ["open","close","ioctl","recvfrom","socket","sendto","pthread_create","recv"]

    #create a target folder
    newpath = f"./Trace results/{target_app}"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    #generate frida trace commands
    commands = []
    for sysc in syscalls:
        if not os.path.exists(f"./Trace results/{target_app}/{sysc}.txt"):
            commands.append(f'frida-trace -U -f {target_app} -i "{sysc}" > "./Trace results/{target_app}/{sysc}.txt"')
        else:
            print(f"./Trace results/{target_app}/{sysc}.txt already exists: skipping")

    run_frida(commands, timeout_seconds=20)