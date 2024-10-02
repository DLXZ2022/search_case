import json
import os
import re
import csv

def process_line_to_csv(line,csv_file):
    try:
        article = json.loads(line)
        content=article.get('content','')
        url=article.get('url','')
        csv_file.writerow([url,content])
    except json.JSONDecodeError:
        print('警告：无法解析的行')

def process_file(file_path,csv_file):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            process_line_to_csv(line,csv_file)
            
def process_dir(dir_path,output_file,num_file=100):
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['content','url'])
        file_count=0
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_count +=1
                json_file_path=os.path.join(root,file)
                process_file(json_file_path,writer)
                print(f"Iter:{file_count}/{num_file}Processing File:{json_file_path}")
                if file_count > num_file:
                    return
                
if __name__ == '__main__':
    wiki_directory='./data/wiki_zh'
    output_csv='./data/wiki_zh.csv'
    num_file=100
    process_dir(wiki_directory,output_csv,num_file)