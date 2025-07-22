import os
import re

def get_etl_project_folders():
    """
    Identifies ETL project folders by checking for the existence of 'go.postgresql.py'.
    """
    project_folders = []
    for folder in os.listdir('.'):
        if os.path.isdir(folder):
            if 'go.postgresql.py' in os.listdir(folder):
                project_folders.append(folder)
    return project_folders

def modify_readme_content(folder, content):
    """
    Modifies the content of a ReadMe.md file according to the specified rules.
    """
    # Convert underline-style H1 to hash-style H1
    content = re.sub(r'^(.*)\n=+$', r'# \1', content, flags=re.MULTILINE)
    # Convert underline-style H2 to hash-style H2
    content = re.sub(r'^(.*)\n-+$', r'## \1', content, flags=re.MULTILINE)

    lines = content.split('\n')
    new_lines = []
    
    # Get title from the first H1
    title = ""
    for line in lines:
        if line.startswith('# '):
            title = line.lstrip('# ').strip()
            break
    
    new_lines.append(f"## [{title}](./{folder})")

    # Process remaining lines
    is_first_h1 = True
    for line in lines:
        if line.startswith('# '):
            if is_first_h1:
                is_first_h1 = False
                continue # Skip the original H1
        
        if line.startswith('#'):
            new_lines.append('#' + line)
        else:
            # Fix relative links
            line = re.sub(r'\[(.*?)\]\(\.\/(.*?)\)', rf'[\1](./{folder}/\2)', line)
            new_lines.append(line)
            
    return '\n'.join(new_lines)

def main():
    """
    Main function to merge the ReadMe.md files.
    """
    etl_folders = get_etl_project_folders()
    merged_content = "# Puffin ETL Importers\n\n"

    for folder in sorted(etl_folders):
        readme_path = os.path.join(folder, 'ReadMe.md')
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                content = f.read()
            modified_content = modify_readme_content(folder, content)
            merged_content += modified_content + '\n\n'

    with open('ImportReadMe.md', 'w') as f:
        f.write(merged_content)

if __name__ == "__main__":
    main()
