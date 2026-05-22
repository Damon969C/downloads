import os
import json
import datetime

def main():
    downloads_dir = 'downloads'
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        
    categorized_files = {}
    
    for root, dirs, files in os.walk(downloads_dir):
        rel_path = os.path.relpath(root, downloads_dir)
        if rel_path == '.':
            category = '根目录'
        else:
            category = rel_path.replace(os.sep, '/')
            
        category_files = []
        
        for filename in files:
            if filename.startswith('.'):
                continue
                
            filepath = os.path.join(root, filename)
            if not os.path.isfile(filepath):
                continue
                
            stat = os.stat(filepath)
            
            size = stat.st_size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 ** 2:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 ** 2):.1f} MB"
                
            dt = datetime.datetime.fromtimestamp(stat.st_mtime)
            date_str = dt.strftime('%Y-%m-%d %H:%M')
            
            category_files.append({
                'name': filename,
                'href': filepath.replace(os.sep, '/'),
                'date': date_str,
                'size': size_str
            })
            
        if category_files:
            category_files.sort(key=lambda x: x['name'])
            categorized_files[category] = category_files
            
    # Optional: ensure '根目录' is first or handled specially
    
    with open('files.json', 'w', encoding='utf-8') as f:
        json.dump(categorized_files, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
