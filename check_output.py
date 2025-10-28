def check_output(test_case_id):
    """
    比对你的程序输出和标准答案。
    :param test_case_id: 测试用例的 ID。
    """
    my_output_path = f"output_data/output_{test_case_id}.txt"
    # 你需要一个生成正确答案的函数或程序
    # 这里我们简化一下，假设你已经有了正确答案文件
    correct_output_path = f"ground_truth/ground_truth_{test_case_id}.txt"
    
    # 你需要自己编写一个函数来生成正确答案文件
    # generate_correct_output(test_case_id)

    try:
        with open(my_output_path, 'r') as my_f, open(correct_output_path, 'r') as correct_f:
            my_lines = my_f.readlines()
            correct_lines = correct_f.readlines()

            if len(my_lines) != len(correct_lines):
                print(f"Test case {test_case_id} FAILED: Line count mismatch.")
                return False

            for i, (my_line, correct_line) in enumerate(zip(my_lines, correct_lines)):
                if my_line.strip() != correct_line.strip():
                    print(f"Test case {test_case_id} FAILED at line {i+1}:")
                    print(f"  Your output:   '{my_line.strip()}'")
                    print(f"  Correct output: '{correct_line.strip()}'")
                    return False
        
        print(f"Test case {test_case_id} PASSED.")
        return True

    except FileNotFoundError:
        print("Required output files not found.")
        return False