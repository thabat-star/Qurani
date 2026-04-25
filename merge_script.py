import json
import os

MAIN_FILE = 'data.json'
TEMP_DIR = 'pending_updates'

def merge():
    if not os.path.exists(TEMP_DIR) or not os.listdir(TEMP_DIR):
        print("لا توجد ملفات دمج.")
        return

    with open(MAIN_FILE, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    playlists_list = full_data.get("playlists", [])

    for filename in os.listdir(TEMP_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(TEMP_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                new_item = json.load(f)
            
            # التعديل هنا: أضفنا is_live أوتوماتيكياً لأي سورة تدمج
            new_audio = {
                "id": new_item['audio_id'],
                "title": new_item['audio_title'],
                "url": new_item['final_url'],
                "is_live": False  # السورة المرفوعة دايماً مش لايف
            }

            found_playlist = None
            for playlist in playlists_list:
                if playlist['playlist_id'] == new_item['playlist_id'] or \
                   playlist['playlist_name'] == new_item['playlist_name']:
                    found_playlist = playlist
                    break
            
            if found_playlist:
                if not any(a['id'] == new_audio['id'] for a in found_playlist['audios']):
                    found_playlist['audios'].append(new_audio)
                    print(f"✅ تم دمج سورة: {new_audio['title']}")
            else:
                new_playlist = {
                    "playlist_id": new_item['playlist_id'],
                    "playlist_name": new_item['playlist_name'],
                    "playlist_image": "https://raw.githubusercontent.com/x0r-1/qurani_app/main/images/default.jpg",
                    "category": new_item['category'],
                    "audios": [new_audio]
                }
                playlists_list.append(new_playlist)
                print(f"✨ تم إنشاء بلاي ليست جديدة لـ: {new_item['playlist_name']}")

    full_data["playlists"] = playlists_list
    with open(MAIN_FILE, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    merge()
