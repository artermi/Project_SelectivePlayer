from PIL import Image, ImageDraw, ImageFont
from player import APlayer,Player
import numpy
import sys, os
from pathlib import Path


def FromArr_png(arr,name):
    data = numpy.zeros((arr.shape[0],arr.shape[1],3), dtype=numpy.uint8)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            #For Bimodal 
            if arr[i,j].isCoop:
                data[i,j] = [153,204,225] if arr[i,j].alp > 0.5 else [0,102,204]
                #Light Blue or Dark Blue
            else:
                data[i,j] = [255,153,153] if arr[i,j].alp > 0.5 else [204,0,0]


            """
            if not arr[i,j].isCoop:
                data[i,j] = [100,100,100] #grey
            else:
                try:
                    nei = arr[i,j].nei
                    if nei == 1:
                        data[i,j] = [255,221,238] #pink
                    elif nei == 3:
                        data[i,j] = [188,188,255] #blue
                    elif nei == 2:
                        data[i,j] = [210,255,210] #green
                    elif nei == 4:
                        data[i,j] = [255,233,210] #orange
                    else:
                        data[i,j] = [255,255,255]

                    if not arr[i,j].strD:
                        data[i,j] = [255,255,255] #white

                except:
                    data[i,j] = [255,255,255] #white 
            """

    data = numpy.repeat(numpy.repeat(data,20,axis = 0),20,axis=1)
    image = Image.fromarray(data)

    textimg = Image.new('RGB',(image.width,50),color = 'white')
    d = ImageDraw.Draw(textimg)
    fnt = ImageFont.truetype('arial.ttf', size = 35)

    fname = name.split('/')[-1]
    if name.find('alp') > -1:
        r,alp,itr = fname.split('_')[1],fname.split('_')[3],fname.split('_')[4]
        towrite = 'r:{}, α:{}, itr:{}'.format(r,alp,itr)
    else:
        r,itr = fname.split('_')[1],fname.split('_')[2]
        towrite = 'r:{}, itr:{}'.format(r,itr)
    #print(towrite)

    d.text((10,10),towrite,font = fnt, fill = (0,0,0))
    note = Image.open('note2.png')
    note = note.resize((image.width, int(note.height * image.width / note.width)),resample=Image.BICUBIC)
    wholeimg = Image.new('RGB',(image.width,image.height + textimg.height + note.height),'white')
    wholeimg.paste(image,(0,0))
    wholeimg.paste(textimg,(0,image.height))
    wholeimg.paste(note,(0,image.height + textimg.height))

    if name.find('/') > -1:
        Path(name.split('/')[0]).mkdir(parents=True, exist_ok=True)

    #wholeimg.show()
    wholeimg.save(name + '.png')

if __name__ == '__main__':
    arr = []
    for i in range(40):
        tmp = []
        for j in range(40):
            if (i + j) % 6 == 0:
                tmp.append(APlayer(False,0))
            elif (i + j) % 6 == 1:
                ap = APlayer(True,0)
                ap.nei = 1
                ap.strD = True
                tmp.append(ap)
            elif (i + j) % 6 == 2:
                ap = APlayer(True,0)
                ap.nei = 3
                ap.strD = True
                tmp.append(ap)
            elif (i + j) % 6 == 3:
                ap = APlayer(True,0)
                ap.nei = 4
                ap.strD = True
                tmp.append(ap)
            elif (i + j) % 6 == 4:
                ap = APlayer(True,0)
                ap.nei = 2
                ap.strD = True
                tmp.append(ap)
            else:
                ap = APlayer(True,0)
                tmp.append(ap)

        arr.append(tmp)
    FromArr_png(numpy.array(arr),'r_5_alp_0.8_000')
