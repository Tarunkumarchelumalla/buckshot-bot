import pytchat
import time
from main import BuckshotRouletteBot

video_id = "VQG2wXx1ugg"
bot = BuckshotRouletteBot("runs/detect/train10/weights/best.pt")

chat = pytchat.create(video_id=video_id)
seen_ids = set()  # Track seen message IDs

print("✅ Watching chat...")

while chat.is_alive():
    chatdata = chat.get()
    if not chatdata.items:
        time.sleep(1)
        continue

    new_messages = []
    for chat_item in chatdata.sync_items():
        if chat_item.id not in seen_ids:
            new_messages.append(chat_item)
            seen_ids.add(chat_item.id)
    print(new_messages)
    if new_messages:
        latest = new_messages[-1]  # Only process the newest one
        print(f"{latest.author.name}: {latest.message}")
        bot.run_command(latest.message)

    time.sleep(1)
