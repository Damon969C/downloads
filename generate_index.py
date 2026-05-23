import os
import json
import datetime

def get_node(tree, rel_path):
    if rel_path == '.':
        return tree
    parts = rel_path.replace(os.sep, '/').split('/')
    current = tree
    for part in parts:
        if part not in current["children"]:
            current["children"][part] = {"files": [], "children": {}}
        current = current["children"][part]
    return current

def main():
    downloads_dir = 'downloads'
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        
    tree = {"files": [], "children": {}}
    
    for root, dirs, files in os.walk(downloads_dir):
        rel_path = os.path.relpath(root, downloads_dir)
        node = get_node(tree, rel_path)
        
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
            
            node["files"].append({
                'name': filename,
                'href': filepath.replace(os.sep, '/'),
                'date': date_str,
                'size': size_str
            })
            
        node["files"].sort(key=lambda x: x['name'])
            
    with open('files.json', 'w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
