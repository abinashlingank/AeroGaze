from Rasyolo.detect import run
for i in range(1,7):
    print(run(weights='Rasyolo/best.pt', source=f'pics/image{i}.jpg', conf_thres=0.9))
