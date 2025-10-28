import subprocess
import os

def compile_java_code(java_code_path):
    """
    编译Java源代码。
    """
    try:
        print("Compiling Java code...")
        subprocess.run(
            ["javac", "-encoding", "UTF-8", f"{java_code_path}/*.java"],
            check=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        print("Compilation successful.")
    except subprocess.CalledProcessError as e:
        print("Compilation failed!")
        print("Error output:", e.stderr)
        return False

def run_java_code(test_case_id, java_code_path):
    """
    运行Java代码，使用指定的输入文件，并将输出保存到文件。
    :param test_case_id: 测试用例的 ID。
    :param java_code_path: Java源代码的目录。
    """
    if not os.path.exists("output_data"):
        os.makedirs("output_data")

    # 运行Java程序并重定向输入输出
    input_file = f"input_data/input_{test_case_id}.txt"
    output_file = f"output_data/output_{test_case_id}.txt"
    
    try:
        print(f"Running test case {test_case_id}...")
        with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
            subprocess.run(
                ["java", "-cp", java_code_path, "Mainclass"], 
                stdin=f_in, 
                stdout=f_out, 
                check=True,
                text=True,
                encoding='utf-8' # 建议添加，以防程序运行时出现编码问题
            )
        print(f"Test case {test_case_id} finished. Output saved to {output_file}.")
        return True
    except subprocess.CalledProcessError as e:
        print("Runtime error occurred!")
        print("Error output:", e.stderr)
        return False
    except FileNotFoundError:
        print(f"Required input file not found: {input_file}")
        return False