import os

def split_models(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_model = []
    current_filename = None

    for line in lines:
        if line.startswith('class '):
            if current_model:
                # 确保 current_filename 不为 None
                if current_filename:
                    with open(os.path.join(output_dir, current_filename), 'w', encoding='utf-8') as f:
                        f.writelines(current_model)
                current_model = []

            # 解析类名并生成文件名
            parts = line.split(' ')
            if len(parts) > 1:
                class_name = parts[1].split('(')[0]
                current_filename = f"{class_name.lower()}.py"
            else:
                current_filename = None

        current_model.append(line)

    if current_model and current_filename:
        with open(os.path.join(output_dir, current_filename), 'w', encoding='utf-8') as f:
            f.writelines(current_model)

if __name__ == "__main__":
    split_models('app/models/models.py', 'app/models')
