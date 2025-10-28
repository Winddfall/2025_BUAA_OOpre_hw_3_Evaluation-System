import argparse
import os
import shutil

from generate_test_case import generate_test_case
from operate_java_code import run_java_code, compile_java_code
from check_output import check_output

def main():
    parser = argparse.ArgumentParser(description="A test suite for Java programs.")
    parser.add_argument("java_path", type=str, help="The path to the Java source code directory.")
    parser.add_argument("-n", "--num_tests", type=int, default=10, 
                        help="The number of test cases to generate and run. (default: 10)")
    parser.add_argument("-op", "--num_operations", type=int, default=100, 
                        help="The number of operations per test case. (default: 100)")
    
    args = parser.parse_args()

    java_code_path = args.java_path
    num_test_cases = args.num_tests # 测试用例数量
    num_operations = args.num_operations # 每个测试用例的操作数量

    # <----------------------- 生成测试用例 ----------------------->
    print("--- Generating test cases ---")
    # 清空输入文件目录/创建输入文件目录
    input_dir = "input_data"
    if os.path.exists(input_dir):
        # 递归删除整个目录树
        shutil.rmtree(input_dir)
    # 重新创建空目录
    os.makedirs(input_dir)

    for i in range(1, num_test_cases + 1):
        generate_test_case(i, num_operations)

    # <----------------------- 编译并运行Java代码 ----------------------->
    print("\n--- Running Java code ---")
    output_dir = "output_data"
    if os.path.exists(output_dir):
        # 递归删除整个目录树
        shutil.rmtree(output_dir)
    # 重新创建空目录
    os.makedirs(output_dir)

    compile_java_code(java_code_path)

    for i in range(1, num_test_cases + 1):
        success = run_java_code(i, java_code_path)
        if not success:
            print(f"Skipping check for test case {i} due to compilation/runtime error.")
            continue

if __name__ == "__main__":
    main()