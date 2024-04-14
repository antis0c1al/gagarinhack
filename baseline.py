from ultralytics import YOLO
import os
model = YOLO('./best.pt')

os.system('''ffmpeg -i ./4.mp4 -vf "select='gt(scene,0.06)',metadata=print:file=time6.txt" -vsync vfr -frame_pts true ./out_tt/%03d.jpg''')

from PIL import Image
import os

path = './out_tt/'
output_path = './combined_4/'

files = os.listdir(path)
files.sort()


for i in range(len(files)):
    if i == 0:
        continue

    img1 = Image.open(path + files[i-1])
    img2 = Image.open(path + files[i])

    if i < len(files) - 1:
        img3 = Image.open(path + files[i+1])
        combined_img = Image.new('RGB', (img1.width + img2.width + img3.width, max(img1.height, img2.height, img3.height)))
        combined_img.paste(img1, (0, 0))
        combined_img.paste(img2, (img1.width, 0))
        combined_img.paste(img3, (img1.width + img2.width, 0))
    else:
        combined_img = Image.new('RGB', (img1.width + img2.width, max(img1.height, img2.height)))
        combined_img.paste(img1, (0, 0))
        combined_img.paste(img2, (img1.width, 0))

    combined_img.save(output_path + files[i])

test_results = model('./combined_4')

start_time = None
end_time = None
first_anomaly = None
prev_time = None
i = 0
FIN=0
with open('./time6.txt', 'r') as file:
    lines = file.readlines()
    current_frame = None
    current_score = None
    for line in lines:
        if line.startswith('frame:'):
            current_frame = int(line.split()[0].split(':')[1])
            time = float(line.split()[2].split(':')[1])
        elif 'lavfi.scene_score=' in line:
            current_score = float(line.split('=')[1])
            anomaly_type = None
            if test_results[i].probs.top1 == 0:
                anomaly_type = "пересвет"
            elif test_results[i].probs.top1 == 1:
                anomaly_type = "расфокус"
            else:
                anomaly_type = "перекрытие"
            i += 1
            if FIN == 1 :
              end_time = time
              print(f'Название первой аномалии: {first_anomaly}, Время старта: {start_time}, Время финиша: {end_time}\n')
              start_time = None
              end_time = None
              first_anomaly = None
              FIN=0
            else:
              if current_score > 0.1:
                  if start_time is None:
                      start_time = time
                      first_anomaly = anomaly_type
                      prev_time = time
                  if time - prev_time < 1:
                    prev_time = time
                    continue
                  elif time - prev_time > 1:
                      FIN = 1
                      prev_time = time