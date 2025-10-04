import os 
import subprocess
import sys

def git_reset_to_remote(repo_path):
    try:
        original_cwd = os.getcwd()
        os.chdir(repo_path)

        print(f"\n---{repo_path}---")
        if not os.path.exists('.git'):
            print(f"not a git {repo_path}")
            os.chdir(original_cwd)
            return False
        
        result = subprocess.run(['git', 'branch', '--show-current'],
                                capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()

        if not current_branch:
            print("cannot define branch")
            os.chdir(original_cwd)
            return False

        result = subprocess.run(['git', 'remote'],
                                capture_output=True, text=True, check=True)
        remote = result.stdout.strip().split('\n')[0] if result.stdout.strip() else 'origin'
        print(f"current branch: {current_branch}")
        print(f"remote: {remote}")

        subprocess.run(['git', 'fetch', remote], check=True)

        subprocess.run(['git', 'reset', '--hard', f'{remote}/{current_branch}'], check=True)
        subprocess.run(['git', 'clean', '-fd'], check=True)
        print(f"{repo_path} is clear")
        os.chdir(original_cwd)
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"error occured {repo_path}:{e}")
        os.chdir(original_cwd)
        return False
    except Exception as e:
        print(f"unknown error {repo_path}:{e}")
        os.chdir(original_cwd)
        return False

def main():
    repo_paths = [
        "/basics-graphics-music",
        "/MC_RISCV_MIREA"
    ]

    cnt = 0
    for raw_path in repo_paths:
        path = cwd + raw_path
        if not os.path.exists(path):
            print(f"folder not exist {path}")
            continue
        
        if git_reset_to_remote(path):
            cnt += 1
    
    print(f"{cnt} repos are cleared")

if __name__ == "__main__":
    main()