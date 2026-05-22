import os
import json
import datetime

def main():
    downloads_dir = 'downloads'
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        
    files_list = []
    
    for filename in os.listdir(downloads_dir):
        # Skip hidden files
        if filename.startswith('.'):
            continue
            
        filepath = os.path.join(downloads_dir, filename)
        
        if os.path.isfile(filepath):
            stat = os.stat(filepath)
            
            # Format size
            size = stat.st_size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 ** 2:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 ** 2):.1f} MB"
                
            # Format date (e.g. 2026-05-22 15:30)
            dt = datetime.datetime.fromtimestamp(stat.st_mtime)
            date_str = dt.strftime('%Y-%m-%d %H:%M')
            
            files_list.append({
                'name': filename,
                'href': f'downloads/{filename}',
                'date': date_str,
                'size': size_str
            })
            
    # Sort files by name
    files_list.sort(key=lambda x: x['name'])
            
    with open('files.json', 'w', encoding='utf-8') as f:
        json.dump(files_list, f, ensure_ascii=False, indent=2)
        
if __name__ == '__main__':
    main()
