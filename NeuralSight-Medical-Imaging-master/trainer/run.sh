python3 -W ignore yolov5/train.py --img 640 --batch 40 --epochs 80 --adam --data /home/vinc3/data/modified_data_folder/yolo5_data/fold_0.xml --device 0 --project ~/data/models_inference/yolov5_fold0/ --weights yolov5m.pt
python3 -W ignore yolov5/train.py --img 640 --batch 40 --epochs 80 --adam --data /home/vinc3/data/modified_data_folder/yolo5_data/fold_1.xml --device 0 --project ~/data/models_inference/yolov5_fold1/ --weights yolov5m.pt
python3 -W ignore yolov5/train.py --img 640 --batch 40 --epochs 80 --adam --data /home/vinc3/data/modified_data_folder/yolo5_data/fold_2.xml --device 0 --project ~/data/models_inference/yolov5_fold2/ --weights yolov5l.pt
python3 -W ignore yolov5/train.py --img 640 --batch 40 --epochs 80 --adam --data /home/vinc3/data/modified_data_folder/yolo5_data/fold_3.xml --device 0 --project ~/data/models_inference/yolov5_fold3/ --weights yolov5l.pt
python3 -W ignore yolov5/train.py --img 640 --batch 40 --epochs 80 --adam --data /home/vinc3/data/modified_data_folder/yolo5_data/fold_4.xml --device 0 --project ~/data/models_inference/yolov5_fold4/ --weights yolov5l.pt